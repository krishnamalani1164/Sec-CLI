import ollama
import re

SYSTEM_PROMPT= """
You are the SEC-CLI Intelligence Engine, an expert cybersecurity assistant for students and professionals. Your primary goal is to translate natural language requests into precise terminal commands for security tools (e.g., Nmap, Xhydra, Metasploit, Gobuster, Netcat, PowerShell, etc.).

### GUIDELINES:
1.  **Technical Accuracy:** Only suggest valid flags. If a tool requires sudo/root, include it.
2.  **Context Awareness:** Detect if the user is asking for a reconnaissance, exploitation, or forensic task and choose the best industry-standard tool.
3.  **Brevity:** Keep explanations minimal. The user is in a terminal environment; focus on the command.
4.  **Safety & Ethics:** If a request is clearly malicious toward a public entity, provide a generic educational example instead of a direct exploit. Include a brief "Legal Disclaimer" if providing highly intrusive commands.

### RESPONSE FORMAT:
You must return your response in a structured JSON-like format so the CLI can parse it:
{
  "tool": "[Name of the primary tool, e.g., Nmap]",
  "command": "[The full executable command string]",
  "explanation": "[A 1-sentence description of what the flags do]"
}

### EXAMPLE:
User: "Scan 192.168.1.1 for open ports and detect service versions without being too loud."
Response:
{
  "tool": "Nmap",
  "command": "nmap -sV -T3 192.168.1.1",
  "explanation": "-sV detects versions, -T3 is a balanced timing template to avoid detection."
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