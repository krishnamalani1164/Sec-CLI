# sec_cli_shell.py
import os
import subprocess
import colorama
from colorama import Fore, Style
from backend.backend_process import BackendProcess

colorama.init()

#Title 
def set_title():
    os.system("title Sec-CLI")


#  Set window title
os.system("title Sec-CLI")

# Initialize Backend
backend = BackendProcess()

print(Fore.CYAN + "SEC_CLI started. Type 'exit' to quit.\n" + Style.RESET_ALL)

while True:
    try:
        user_input = input(Fore.GREEN + "sec-cli> " + Style.RESET_ALL)
    except KeyboardInterrupt:
        print()
        break

    if not user_input.strip():
        continue

    if user_input.strip().lower() in ["exit", "quit"]:
        break

    # Step 1:  Try native OS execution FIRST
    try:
        result = subprocess.run(
            user_input,
            shell = True,
            capture_output = True,
            text = True
        )

        #If command executed successfully -> done
        if result.returncode == 0:
            if result.stdout:
                print(result.stdout)
            continue
        # if error is NOT "command not recognized", show error
        stderr = result.stderr.lower()
        if "not recognized" not in stderr:
            print(result.stderr)
            continue

    except Exception:
        pass # fall back to NLP pipeline

    # Send input to backend
    result = backend.process_prompt(user_input)

    tool = result.get("tool")
    command = result.get("command")

    # Case 1: Natural Language handled by SEC_CLI
    if not command:
        print(Fore.RED + "❌ Unable to interpret input as a command." + Style.RESET_ALL)
        continue


    print(Fore.YELLOW + f"🔧 Tool Detected: {tool}" +Style.RESET_ALL)
    print(Fore.MAGENTA + f"⚙ Generated Command: {command}" + Style.RESET_ALL)

    subprocess.Popen(
        command,
        shell=True
    ).wait()
