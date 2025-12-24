import os
import subprocess
import colorama
import threading
import re
from colorama import Fore, Style

colorama.init()
os.system("title Sec-CLI")

PROMPT_PREFIX = "?"
backend_inst = None

def load_backend():
    global backend_inst
    try:
        from backend.backend_process import BackendProcess
        backend_inst = BackendProcess()
        print(f"\n{Fore.CYAN}[SYSTEM] NLP Backend ready!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR] Failed to load backend: {e}{Style.RESET_ALL}")

bg_thread = threading.Thread(target=load_backend, daemon=True)
bg_thread.start()

def is_natural_language(text):
    text_lower = text.lower()
    nl_indicators = ["how", "what", "why", "can", "please", "find", "search", "explain", "tell"]
    has_cli_flags = bool(re.search(r"[-/]\w+", text))
    word_count = len(text.split())
    return (any(word in text_lower for word in nl_indicators) or word_count > 4) and not has_cli_flags

def run_ai_logic(prompt_text):
    """Encapsulated AI processing logic to be reused in fallbacks."""
    if backend_inst is None:
        print(Fore.YELLOW + "Backend still initializing..." + Style.RESET_ALL)
        return False

    print(Fore.YELLOW + f"🤖 Processing as prompt: {prompt_text}" + Style.RESET_ALL)
    result = backend_inst.process_prompt(prompt_text)
    generated_cmd = result.get("command")

    if generated_cmd:
        print(Fore.CYAN + f"🔧 Tool: {result.get('tool')}")
        print(Fore.MAGENTA + f"⚙ Proposed: {generated_cmd}" + Style.RESET_ALL)
        confirm = input("Execute? (y/n): ").lower()
        if confirm == 'y':
            subprocess.run(generated_cmd, shell=True)
        return True
    return False

print(Fore.CYAN + "SEC-CLI [Smart Hybrid Mode]")
print(f"Priority: Explicit Prefix (?) -> Standard Command -> Heuristics -> AI Fallback\n")

while True:
    try:
        cwd = os.getcwd()
        user_input = input(f"{Fore.GREEN}{cwd}> {Style.RESET_ALL}").strip()
    except KeyboardInterrupt:
        break

    if not user_input: continue
    if user_input.lower() in ["exit", "quit"]: break

    # --- 1. CD Interception ---
    if user_input.lower().startswith("cd "):
        try:
            os.chdir(user_input[3:].strip().strip('"'))
            continue
        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            continue

    # --- 2. Explicit & Heuristic Detection (Early Exit to AI) ---
    is_explicit = user_input.startswith(PROMPT_PREFIX)
    if is_explicit or is_natural_language(user_input):
        clean_text = user_input[len(PROMPT_PREFIX):].strip() if is_explicit else user_input
        run_ai_logic(clean_text)
        continue

    # --- 3. Direct Execution with Fallback ---
    # We use shell=True. If returncode != 0, it likely failed.
    try:
        # Note: We use subprocess.run without capturing output so user sees 
        # errors like "'grep' is not recognized..."
        result = subprocess.run(user_input, shell=True)
        
        # If the command failed (exit code non-zero), trigger the final fallback
        if result.returncode != 0:
            print(Fore.DIM + "Command failed. Attempting AI interpretation..." + Style.RESET_ALL)
            if not run_ai_logic(user_input):
                print(Fore.RED + "AI could not resolve the failed command." + Style.RESET_ALL)
                
    except Exception as e:
        # Emergency fallback if subprocess itself crashes
        run_ai_logic(user_input)