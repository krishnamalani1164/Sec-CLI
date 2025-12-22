import ollama

class LocalLLM:
    def __init__(self, model: str = "mistral"):
        # The library uses a default client, but you can also specify 
        # a host if your Ollama server is running elsewhere.
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Generate text using the official Ollama Python library.
        """
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
            )

            print(f"response is {response}")
            return response['response'].strip()
        except Exception as e:
            raise RuntimeError(f"Ollama Error: {e}")

# Example Usage:
# llm = LocalLLM()
# print(llm.generate("Why is the sky blue?"))