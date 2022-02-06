"""
Connects an available port to your local machine and then runs tensorboard on that
port.
"""

import argparse
import random
import socket
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("logdir")
parser.add_argument(
    "-l",
    "--local_port",
    type=int,
    help="which port your local machine forwarded to the remote server when ssh-ing",
)
parser.add_argument(
    "-u",
    "--user",
    help="the username you use on your local laptop/desktop you ssh'd from",
)
parser.add_argument(
    "-r",
    "--reconfigure",
    action="store_true",
    help="use this flag to update info about local machine",
)
args = parser.parse_args()

LOCAL_USERNAME = "<LOCAL_USERNAME>"
LOCAL_PORT = "<LOCAL_PORT>"

if "<" in LOCAL_USERNAME or "<" in str(LOCAL_PORT) or args.reconfigure:
    print(f"LOCAL_PORT and LOCAL_USERNAME currently undefined, or --reconfigure called")
    local_user = input("Enter the username of your LOCAL machine (NOT this one): ")
    local_port = input("Enter local port used with 'ssh -R' to ssh to this machine: ")
    with open(__file__) as f:
        data = f.read()
    new_data = []
    for line in data.splitlines():
        if line.startswith("LOCAL_USERNAME ="):
            line = f"LOCAL_USERNAME = '{local_user}'"
        elif line.startswith("LOCAL_PORT ="):
            line = f"LOCAL_PORT = {local_port}"
        new_data.append(line)
    with open(__file__, "w") as f:
        f.write("\n".join(new_data))
    print("File updated!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"PLEASE RUN: ssh-copy-id -p {local_port} {local_user}@localhost")
    print("to enable port forwarding to local machine via pubkey auth.")
    print("(it will skip copying if key already exists on local machine.)")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    exit()

print(f"Local port: {LOCAL_PORT}\nLocal username: {LOCAL_USERNAME}")
print(f"Run this script with --reconfigure if you want to update the above values")

local_port = LOCAL_PORT if args.local_port is None else args.local_port
user = LOCAL_USERNAME if args.user is None else args.user
logdir = args.logdir

# Find an available port to host the tensorboard
print("Searching for available port...")
viz_ports = list(range(8000, 9001))
random.shuffle(viz_ports)
found = False
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    for p in viz_ports:
        if s.connect_ex(("localhost", p)) != 0:
            tb_port = p
            found = True
            break
if found:
    print(f"Port found: {tb_port}\n")
else:
    print("NO AVAILABLE PORTS?!?!?!?!?")
    exit()


# Check for other tmux sessions this script may have made that didn't get killed
# (should happen very rarely if at all), or if you just have another terminal with
# this script running in it. This will error if no tmux sessions are active yet,
# so we wrap it in a try except.
try:
    out = subprocess.check_output("tmux ls", shell=True).decode("utf-8")
    existing_jobs = [line.split(":")[0] for line in out.splitlines() if "rssh_" in line]
    if existing_jobs:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!! WARNING !!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("You have existing tmux sessions created from this script:")
        for j in existing_jobs:
            print(j)
        print()
except:
    pass

# Forward the tensorboard port back to local machine in the background
print("Connecting to local machine...")
tmux_session_name = f"rssh_{tb_port}"
cmd = (
    f"tmux new -s {tmux_session_name} -d "
    f"ssh -R {tb_port}:localhost:{tb_port} -p {local_port} {user}@localhost  "
    '-o "StrictHostKeyChecking no"'
)
subprocess.check_call(cmd, shell=True)
print("Executed:\n", cmd, "\n")

# Now that ports are connected, run tensorboard.
print(f"Tensorboard will soon be available locally at: http://localhost:{tb_port}/")
print("Running tensorboard...\n")
try:
    # Run tensorboard command
    cmd = f"tensorboard  --port {tb_port} --logdir {logdir}"
    print("Executing:\n", cmd)
    subprocess.check_call(cmd, shell=True)
finally:
    # Kill the tmux session if user kill this python script
    cmd = f"tmux kill-session -t {tmux_session_name}"
    print("\nExecuting:\n", cmd)
    subprocess.check_call(cmd, shell=True)
    print("Successfully killed rssh tmux! Have a good day.")
