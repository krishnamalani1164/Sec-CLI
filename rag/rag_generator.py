from retriever import RAGRetriever
from context_builder import build_context
from llm.llm_client import LocalLLM


class RAGCommandGenerator:
    def __init__(self, k: int = 3, model: str = "mistral"):
        # EVERYTHING using self MUST be inside __init__
        self.retriever = RAGRetriever(k=k)
        self.llm = LocalLLM(model=model)

    def generate(self, user_prompt: str) -> str:
        #Step 1: Retrieve relevant examples
        retrieved = self.retriever.retrieve(user_prompt)

        if not retrieved:
            return ""

        # Step 2: Build RAG context
        context_prompt = build_context(retrieved, user_prompt)

        print("Context Prompt:",context_prompt)
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

if __name__ == "__main__":
    # 1. Initialize the Generator
    # 'k=2' retrieves the top 2 closest matches from your Vector Store
    generator = RAGCommandGenerator(k=2, model="mistral")

    # 2. Define test scenarios
    test_queries = [
        "I need to scan 192.168.1.1 for open ports using nmap",
        "Show me the command to check for vulnerabilities on a subnet with nmap"
    ]

    print("="*50)
    print("RAG COMMAND GENERATOR TEST SESSION")
    print("="*50)

    for i, user_query in enumerate(test_queries, 1):
        print(f"\n[Test {i}] User Prompt: {user_query}")
        
        try:
            # The generate method prints 'Context Prompt' and 'Cleaned Command' internally
            final_command = generator.generate(user_query)
            
            print(f"Final Result: {final_command}")
            print("-" * 30)
            
        except Exception as e:
            print(f"Error during generation: {e}")

    print("\nTest session complete.")