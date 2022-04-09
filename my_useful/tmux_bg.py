import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("session_name")
parser.add_argument("cmd", nargs="+")
args = parser.parse_args()

cmd = " ".join(args.cmd)
tmux_cmd = f"tmux new -s {args.session_name} -d '{cmd}'"
print("Executing:\n", tmux_cmd)
subprocess.check_call(tmux_cmd, shell=True)
