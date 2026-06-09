import csv
import os
from datetime import datetime

from classifier.classifier import classify_tool
from rag.rag_generator import RAGCommandGenerator
from llm.llm_client import LocalLLM

BASE_TOOL_LIST = ["nmap","snort","xhydra"]

LOG_FILE = "logs/sec_cli_logs.csv"


class BackendProcess:
    """
    BackendProcess acts as the orchestrator between
    CLI, Classifier, RAG-based Command Generator, and Logger.
    """

    def __init__(self):
        self.__init__logger()
        # Initialize RAG-based generator once
        self.generator = RAGCommandGenerator(k=3, model="mistral")
        self.sft_model= LocalLLM(model="mistral")

    def __init__logger(self):
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "user_prompt",
                    "predicted_tool",
                    "generated_command",
                    "execution_status"
                ])

    def _log(self, prompt, tool, command, status):
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                prompt,
                tool,
                command,
                status
            ])

    def process_prompt(self, prompt: str, current_os: str = "Linux") -> dict:
        """
        Takes user prompt and returns:
        {
            tool: <predicted_tool>
            command: <generated_command>
        }
        """

        # Step 1: Tool classification
        classification = classify_tool(prompt)
        tool_name = classification["tool"]
        confidence = classification["confidence"]

        # Native command check (simple heuristic)
        native_cmds = ["dir", "cd", "pwd", "ipconfig", "ls", "echo"]

        if prompt.strip().split()[0] in native_cmds:
            return {"tool": "native", "command": prompt}

        # Low confidence → reject politely
        if confidence < 0.40:
            print( "⚠ Low confidence in tool prediction. Aborting command generation.")
            self._log(prompt, "unknown", "", "low_confidence")
            return {"tool": None, "command": None}
        
        user_prompt = f"Generate a {tool_name} command for the following request:\n{prompt}"

        # system_prompt= """ You are a hel-pful assistant for regular office work. You will be provided with a a persons user profile and 
        # list of permissions
        # try to be as helpful as possible but only provide repsonses for which the user has permissions. If the user does not have permissions to perform the task, respond with 'Permission Denied'.
        # """

        ##User prompt:  The following user has made a query as follows: {prompt}. The user is currently on {current_os} and has the following permissions: [list of permissions]. Genera.
        if tool_name in BASE_TOOL_LIST:
            
            print(f"Using SFT-based generation for tool: {tool_name}")
            command = self.sft_model.generate(user_prompt)
            self._log(prompt, tool_name, command, "generated")
        else:
        # Step 2: RAG + LLM command generation
            try:
                print(f"Using RAG-based generation for tool: {tool_name}")
                command = self.generator.generate(user_prompt)
                
            except Exception as e:
                self._log(prompt, tool_name, "", "generation_error")
                return {
                    "tool": tool_name,
                    "command": None
                }

        if not command:
            self._log(prompt, tool_name, "", "no_command_generated")
            return {
                "tool": tool_name,
                "command": None
            }

        # Log successful generation
        self._log(prompt, tool_name, command, "generated")

        return {
            "tool": tool_name,
            "command": command
        }