"""
Execute scp using a default remote host so you don't have to type it out.
By default, the first arg represents the remote path (src) and the second arg represents
the local path (dst). You can use -s to reverse this.
"""
import argparse
import os
import subprocess

REMOTE_HOST = os.environ["DEFAULT_REMOTE_HOST"]

parser = argparse.ArgumentParser()
parser.add_argument("src")
parser.add_argument("dst", nargs="?", default=os.getcwd())
parser.add_argument(
    "-s",
    "--send",
    action="store_true",
    help="indicates that file will be sent from local to remote",
)
parser.add_argument("-n", "--hostname", help="Change hostname. Just use scp, man.")
args = parser.parse_args()

# If "~" was in the arg, this script sees it as being replaced $HOME
# Here, we reverse this replacement
src = args.src.replace(os.environ["HOME"], "~")
dst = args.dst.replace(os.environ["HOME"], "~")

if args.send:
    cmd = f"scp -r {src} {REMOTE_HOST}:{dst}"
else:
    cmd = f"scp -r {REMOTE_HOST}:{src} {dst}"

print("Remote host:", REMOTE_HOST)
print("Executing:\n", cmd)

# Need to use shell=True so that "~" maps to $HOME again
# This is important if the remote path had a "~", because that
# should NOT be replaced by the
subprocess.check_call(cmd, shell=True)
