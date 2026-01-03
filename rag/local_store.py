import os
import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


CORE_PATH = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(CORE_PATH, "command_rows_with_intent.jsonl")

INDEX_PATH = os.path.join(CORE_PATH, "local_index.faiss")
META_PATH = os.path.join(CORE_PATH, "local_meta.pkl")
TOOL_INDEX_PATH = os.path.join(CORE_PATH, "tool_index.pkl")


class LocalVectorStore:
    """
    Hard filter  : tool
    Embedding   : intent + command_category
    Metadata    : commands, flags, parameters, constraints, safety notes
    """

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.metadata = []
        self.tool_index = {}

    # ---------- JSONL Loader ----------
    def _load_jsonl(self, path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)

    # ---------- Embedding Text ----------
    def _build_embedding_text(self, record):
        """
        Tool is intentionally excluded.
        Only semantic intent + category.
        """
        return f"""
Intent:
{record.get('intent', '')}

Command Category:
{record['command_category']}
""".strip()

    # ---------- Build Index ----------
    def build(self):
        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

        records = list(self._load_jsonl(DATASET_PATH))
        if not records:
            raise ValueError("Dataset is empty")

        texts = []
        self.metadata = []
        self.tool_index = {}

        for idx, r in enumerate(records):
            required = {"tool", "command_category", "intent"}
            if not required.issubset(r.keys()):
                raise ValueError(f"Invalid schema in record {idx}")

            # Embedding text
            texts.append(self._build_embedding_text(r))

            # Metadata (rich, non-embedded)
            self.metadata.append({
                "tool": r["tool"],
                "command_category": r["command_category"],
                "intent": r.get("intent", ""),
                "command_patterns": r.get("command_patterns", []),
                "parameters": r.get("parameters", []),
                "optional_flags": r.get("optional_flags", []),
                "constraints": r.get("constraints", []),
                "safety_notes": r.get("safety_notes", "")
            })

            # Hard filter index
            self.tool_index.setdefault(r["tool"], []).append(idx)

        print(f"[LocalVectorStore] Encoding {len(texts)} records...")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True
        ).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # Persist
        faiss.write_index(self.index, INDEX_PATH)

        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

        with open(TOOL_INDEX_PATH, "wb") as f:
            pickle.dump(self.tool_index, f)

        print(f"[✓] Indexed {len(self.metadata)} records")
        print(f"[✓] Tools indexed: {len(self.tool_index)}")

    # ---------- Load Index ----------
    def load(self):
        if not (
            os.path.exists(INDEX_PATH)
            and os.path.exists(META_PATH)
            and os.path.exists(TOOL_INDEX_PATH)
        ):
            raise FileNotFoundError("Vector store not found. Build it first.")

        self.index = faiss.read_index(INDEX_PATH)

        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        with open(TOOL_INDEX_PATH, "rb") as f:
            self.tool_index = pickle.load(f)

    # ---------- Search ----------
    def search(self, query: str, tool: str, k: int = 3):
        """
        Hard filter by tool
        Semantic rank by intent + category
        """
        if self.index is None:
            self.load()

        if tool not in self.tool_index:
            return []

        query_emb = self.model.encode(
            [query],
            normalize_embeddings=True
        ).astype("float32")

        candidate_ids = set(self.tool_index[tool])

        # Over-fetch then filter
        fetch_k = min(len(self.metadata), max(k * 5, 20))
        scores, indices = self.index.search(query_emb, fetch_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx in candidate_ids:
                item = self.metadata[idx].copy()
                item["score"] = float(score)
                results.append(item)

            if len(results) >= k:
                break

        return results


# ---------- Test Harness ----------
if __name__ == "__main__":
    lvs = LocalVectorStore()

    if not os.path.exists(INDEX_PATH):
        print("[*] Building vector index...")
        lvs.build()
    else:
        print("[*] Loading existing index...")
        lvs.load()

    query = "extract database information from a vulnerable parameter"
    tool = "sqlmap"

    print(f"\n[Test] Query: {query}")
    print(f"[Test] Tool filter: {tool}")

    results = lvs.search(query=query, tool=tool, k=3)

    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} (score={r['score']:.4f}) ---")
        print(f"Tool:      {r['tool']}")
        print(f"Category:  {r['command_category']}")
        print(f"Intent:    {r['intent']}")
        print(f"Commands:  {r['command_patterns']}")
        print(f"Flags:     {r['optional_flags']}")
        print(f"Params:    {r['parameters']}")
        print(f"Safety:    {r['safety_notes']}")
