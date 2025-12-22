import ollama
import re

class LocalLLM:
    def __init__(self, model: str = "mistral"):
        # Using the Client instance for better configuration control
        self.client = ollama.Client()
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Generates a response and extracts the first bash command found.
        """
        try:
            # Call the Ollama API
            response = self.client.generate(
                model=self.model,
                prompt=prompt
            )
            raw_text = response['response']
            
            # Extract the first bash block
            return self._extract_bash(raw_text)
            
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

    def _extract_bash(self, text: str) -> str:
        """
        Internal helper to parse markdown bash blocks.
        """
        # Pattern looks for ```bash, captures content, stops at first ```
        pattern = r"```bash\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        return "No bash command found in the response."

# --- Example Usage ---
if __name__ == "__main__":
    llm = LocalLLM(model="mistral")
    user_prompt = "Give me an nmap command to scan 172.16.92.23"
    
    command = llm.generate_command(user_prompt)
    print(f"Extracted Command: {command}")