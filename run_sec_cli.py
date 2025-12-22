# run_sec_cli.py
import subprocess
import sys
import os

python_exe = sys.executable
script_path = ".\sec_cli_shell.py"


# Wrap paths in double quotes to handle spaces and drive letters
command = f'{python_exe} {script_path}'

subprocess.Popen(
    ["cmd.exe", "/k", command],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
