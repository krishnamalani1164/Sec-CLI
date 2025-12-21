import subprocess

class LocalLLM:
    def __init__(self, model: str = "mistral"):
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Generate text using local Ollama LLM.
        """
        result = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt,
            text=True,
            capture_output=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()
