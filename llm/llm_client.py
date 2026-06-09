import ollama
import re

SYSTEM_PROMPT= """
You are the SEC-CLI Intelligence Engine, an expert cybersecurity mentor for students and professionals.

### OPERATIONAL CONSTRAINTS:
1. **OS Detection:** If the user doesn't specify an OS, provide a Linux-compatible command (using sudo where needed). If they mention Windows, provide PowerShell-compatible syntax.
2. **Pathing:** Use universal path separators or mention that paths may need adjustment.
3. **No Semicolons:** Use '&&' for chaining in both Linux and Windows (PowerShell/CMD both support this).

### CROSS-PLATFORM EXAMPLE:
User: "Run a quick service scan on 10.0.0.5 and save it to results.txt"

Response (Linux/Unix):
{
  "tool": "Nmap",
  "command": "sudo nmap -sV -F 10.0.0.5 -oN results.txt",
  "explanation": "-sV detects service versions, -F is 'Fast mode' (top 100 ports), and -oN saves to text.",
  "safety_note": "Requires sudo on Linux for raw packet access. Fast scan is less likely to be blocked by firewalls than a full port scan."
}

Response (Windows/PowerShell):
{
  "tool": "Nmap",
  "command": "nmap -sV -F 10.0.0.5 -oN results.txt",
  "explanation": "-sV detects service versions, -F scans the top 100 ports, and -oN outputs to results.txt.",
  "safety_note": "On Windows, ensure you are running the terminal as Administrator for features like OS fingerprinting (-O) or SYN scans (-sS)."
}
"""

class LocalLLM:
    def __init__(self, model: str = "mistral"):
        # Using the Client instance for better configuration control
        self.client = ollama.Client()
        self.model = model
        self.system_prompt = SYSTEM_PROMPT
    def generate(self, prompt: str) -> str:
        """
        Generates a response and extracts the first bash command found.
        """
        try:
            # Call the Ollama API
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                system=self.system_prompt,
            )
            raw_text = response['response']
            
            print(f"Ollama Raw Response: {raw_text}")  # Debugging output
            # Extract the first bash block
            return self.extract_command(raw_text)
            
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
    
    def extract_command(self, response: str) -> str:
        """
        Extracts the command from the structured JSON-like response.
        """
        pattern = r'"command":\s*"(.*?)"'
        match = re.search(pattern, response)
        
        if match:
            return match.group(1).strip()
        
        return "No command found in the response."

# --- Example Usage ---
if __name__ == "__main__":
    llm = LocalLLM(model="mistral")
    user_prompt = "Give me an nmap command to scan 172.16.92.23"
    
    command = llm.generate(user_prompt)
    print(f"Extracted Command: {command}")