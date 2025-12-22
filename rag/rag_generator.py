# from rag.retriever import RAGRetriever
# from rag.context_builder import build_context
from llm.llm_client import LocalLLM


class RAGCommandGenerator:
    def __init__(self, k: int = 3, model: str = "mistral"):
        # EVERYTHING using self MUST be inside __init__
        #self.retriever = RAGRetriever(k=k)
        self.llm = LocalLLM(model=model)

    def generate(self, user_prompt: str) -> str:
        # Step 1: Retrieve relevant examples
        # retrieved = self.retriever.retrieve(user_prompt)

        # if not retrieved:
        #     return ""

        # # Step 2: Build RAG context
        # context_prompt = build_context(retrieved, user_prompt)

        # # Step 3: Generate command using LLM
        # command = self.llm.generate(context_prompt)
        # Step 3: Generate command using LLM
        command = self.llm.generate(user_prompt)

        cleaned = command.strip().splitlines()[0]
        print("Cleaned Command",cleaned)

        # Remove common LLM prefixes
        for prefix in ["Command:", "command:", "CLI:", "Output:"]:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()

        return cleaned

