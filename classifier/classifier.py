
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os

DATASET_PATH = os.path.join("data", "security_nlp_cli_10000.csv")
SIMILARITY_THRESHOLD = 0.45   # robust default

class EmbeddingClassifier:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._load_dataset()

    def _load_dataset(self):
        df = pd.read_csv(DATASET_PATH)

        # ---- SAFETY CHECK ----
        required_cols = {"nl_prompt", "tool"}
        if not required_cols.issubset(df.columns):
            raise ValueError(
                f"Dataset must contain {required_cols}, found {set(df.columns)}"
            )

        # expected columns : prompt,tool
        self.prompts = df["nl_prompt"].astype(str).tolist()
        self.tools = df["tool"].astype(str).tolist()

        # Pre compute embeddings
        self.prompt_embeddings = self.model.encode(
            self.prompts,
            convert_to_numpy=True,
            show_progress_bar=True
        )


    def predict_tool(self,user_prompt: str) -> str:
        user_embedding = self.model.encode(
            [user_prompt],
            convert_to_numpy = True
        )

        similarities = cosine_similarity(
            user_embedding,
            self.prompt_embeddings
        )[0]

        best_idx = int(np.argmax(similarities))
        best_score = float(similarities[best_idx])

        return {
            "tool" : self.tools[best_idx],
            "confidence" : best_score
        }
    

# Singleton instance (important for performance)
_classifier = EmbeddingClassifier()

def classify_tool(prompt: str) -> dict:
    return _classifier.predict_tool(prompt)
