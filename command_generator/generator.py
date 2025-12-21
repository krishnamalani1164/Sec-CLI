
import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

DATASET_PATH = os.path.join("data", "security_nlp_cli_10000.csv")

class DatasetCommandGenerator:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._load_dataset()
    
    def _load_dataset(self):
        df = pd.read_csv(DATASET_PATH)

        # Required columns
        required = {"tool", "nl_prompt", "cli_command_demo"}
        if not required.issubset(df.columns):
            raise ValueError(f"Dataset missing columns: {required}")

        self.df = df
        self.prompts = df["nl_prompt"].astype(str).tolist()
        self.commands = df["cli_command_demo"].astype(str).tolist()

        self.embeddings = self.model.encode(
            self.prompts,
            convert_to_numpy=True,
            show_progress_bar=False
        )

    def generate(self,user_prompt : str ,predicted_tool: str) -> str | None:
        #Filter dataset by tool
        subset = self.df[self.df["tool"] == predicted_tool]

        if subset.empty:
            return None

        prompts = subset["nl_prompt"].astype(str).tolist()
        commands = subset["cli_command_demo"].astype(str).tolist()

        prompt_embs = self.model.encode(prompts, convert_to_numpy=True)
        user_emb = self.model.encode([user_prompt], convert_to_numpy=True)

        sims = cosine_similarity(user_emb, prompt_embs)[0]
        best_idx = int(np.argmax(sims))

        return commands[best_idx]
    

# Singleton
_generator = DatasetCommandGenerator()

def generate_command(prompt: str, tool: str) -> str | None:
    return _generator.generate(prompt, tool)