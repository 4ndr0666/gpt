#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

os.environ["_CTX"] = "1"

def run_command(cmd, timeout=7200):
    try:
        result = subprocess.run(["timeout", str(timeout)] + cmd, capture_output=True, text=True, check=False)
        return result.returncode
    except:
        return 1

def main():
    print("init sequence started.")

    bootstrap_cmd = ["bash", "setup_initial.sh"]
    if len(sys.argv) > 1:
        bootstrap_cmd.append(sys.argv[1])
    run_command(bootstrap_cmd)

    gen_args = ["python3", "generate_loader.py"] + sys.argv[1:]
    exit_code = run_command(gen_args, timeout=86400)

    Path("./outputs/_ctx.json").write_text('{"t": "' + datetime.now().isoformat() + '", "s": "complete"}')
    print("init sequence complete.")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
