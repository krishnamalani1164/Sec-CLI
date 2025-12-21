# run_sec_cli.py
import subprocess
import sys
import os

python_exe = sys.executable
script_path = os.path.abspath("sec_cli_shell.py")

subprocess.Popen(
    ["cmd.exe", "/k", f"{python_exe} {script_path}"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
