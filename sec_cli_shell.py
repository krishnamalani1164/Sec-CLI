# sec_cli_shell.py
import os
import subprocess
import colorama
import threading
from colorama import Fore, Style
#from backend.backend_process import BackendProcess

colorama.init()

#  Set window title
os.system("title Sec-CLI")

# Initialize Backend
def load_backend():
    print("Loading backend in background...")
    # The import happens inside the function
    from backend.backend_process import BackendProcess
    global backend_inst
    backend_inst = BackendProcess()
    print("Backend ready! Press enter to return to CLI")

# Start the thread
bg_thread = threading.Thread(target=load_backend, daemon=True)
bg_thread.start()

# Your main code continues immediately here
print("Main interface is running...")

#backend = BackendProcess()

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
        else:
            stderr = result.stderr.lower()
            print(stderr)
            if "not recognized" not in stderr:
                print(result.stderr)
                continue 
        

    except Exception:
        pass
        # if error is NOT "command not recognized", show error
        # fall back to NLP pipeline

    print("command not recognised falling back to prompt mode")

    



    # Send input to backend
    result = backend_inst.process_prompt(user_input)

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
