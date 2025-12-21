import os
import pickle
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

DATASET_PATH = os.path.join("data", "security_nlp_cli_10000.csv")
INDEX_PATH = os.path.join("rag", "local_index.faiss")
META_PATH = os.path.join("rag", "local_meta.pkl")

class LocalVectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.metadata = []

    def build(self):
        df = pd.read_csv(DATASET_PATH)

        required_cols = {"nl_prompt", "cli_command_demo", "safety_note", "tool"}
        if not required_cols.issubset(df.columns):
            raise ValueError(
                f"Dataset must contain {required_cols}, found {set(df.columns)}"
            )

        texts = df["nl_prompt"].astype(str).tolist()

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        ).astype("float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        # Store metadata aligned with FAISS ids
        self.metadata = df[
            ["nl_prompt", "cli_command_demo", "safety_note", "tool"]
        ].to_dict(orient="records")

        # Persist to disk
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

        print(f"[LocalVectorStore] Indexed {len(self.metadata)} records")

    def load(self):
        if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
            raise FileNotFoundError("Local vector DB not found. Build it first.")

        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query: str, k: int = 3):
        if self.index is None:
            self.load()

        query_emb = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(query_emb, k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            item = self.metadata[idx].copy()
            item["distance"] = float(dist)
            results.append(item)

        return results