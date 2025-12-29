import os
import pickle
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

CORE_PATH= os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(CORE_PATH, "..\data", "security_nlp_cli_10000.csv")
INDEX_PATH = os.path.join(CORE_PATH, "local_index.faiss")
META_PATH = os.path.join(CORE_PATH, "local_meta.pkl")

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
    
if __name__ == "__main__":
    # # 1. Setup environment: Create necessary directories
    # os.makedirs("data", exist_ok=True)
    # os.makedirs("rag", exist_ok=True)

    # # 2. Check if the dataset exists in the expected location
    # # If the file is in the current directory, we move/copy it to the 'data' folder
    # source_file = "security_nlp_cli_10000.csv"
    # if os.path.exists(source_file) and not os.path.exists(DATASET_PATH):
    #     import shutil
    #     shutil.copy(source_file, DATASET_PATH)
    #     print(f"Copied {source_file} to {DATASET_PATH}")

    # 3. Initialize and Build the Vector Store
    lvs = LocalVectorStore()
    
    # Check if we need to build or just load
    if not os.path.exists(INDEX_PATH):
        print("Building the vector index... (This may take a minute)")
        lvs.build()
    else:
        print("Loading existing index...")
        lvs.load()

    # 4. Perform a test search
    test_query = "How can I perform a quick scan of the top 100 ports on 192.168.1.1?"
    print(f"\n[Test] Searching for: '{test_query}'")
    
    results = lvs.search(test_query, k=2)

    # 5. Display results
    for i, res in enumerate(results):
        print(f"\n--- Result {i+1} (Distance: {res['distance']:.4f}) ---")
        print(f"Tool:    {res['tool']}")
        print(f"Prompt:  {res['nl_prompt']}")
        print(f"Command: {res['cli_command_demo']}")
        print(f"Safety:  {res['safety_note']}")
    
