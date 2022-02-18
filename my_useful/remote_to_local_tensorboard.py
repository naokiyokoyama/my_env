"""
Connects an available port to your local machine and then runs tensorboard on that
port.
"""

import argparse
import json
import os.path as osp
import random
import socket
import subprocess

JSON_FILE = osp.abspath(__file__).replace(".py", ".json")
if osp.isfile(JSON_FILE):
    with open(JSON_FILE) as f:
        json_data = json.load(f)
else:
    json_data = None

parser = argparse.ArgumentParser()
parser.add_argument("logdir")
parser.add_argument(
    "-r",
    "--reconfigure",
    action="store_true",
    help="use this flag to update info about local machines",
)
parser.add_argument(
    "-l",
    "--local_port",
    type=int,
    help="override port to connect to on local machine in case RemoteForward fails",
)
parser.add_argument(
    "-n",
    "--nickname",
    help="which local machine to connect to",
)
args = parser.parse_args()

if json_data is None or args.reconfigure:
    if json_data is None:
        json_data = {}
        print(f"First time setup! Initializing {JSON_FILE}...")
    else:
        print("--reconfigure was called!")

    # Ask for and gather info
    local_user = input("Enter your USERNAME on your LOCAL machine (NOT this one): ")
    local_port = input("Enter RemoteForward port used to ssh to this machine: ")
    nickname = input("Enter a nickname for local machine: ")
    default = ""
    while default.lower() not in ["y", "n"]:
        default = input("Set as default? [Y/n]: ")
        if not default:
            default = "y"
    current_tb_executable = json_data.get("_tb_executable", "tensorboard")
    tb_executable = input(
        "Path to tensorboard executable (run 'which tensorboard' in a (conda) "
        "environment that has tensorboard installed)"
        f" (default: '{current_tb_executable}'): "
    )
    if not tb_executable:
        tb_executable = current_tb_executable

    # Save data to JSON
    if not default.lower() == "n":
        json_data["_default_local_machine"] = nickname
    if nickname in json_data:
        print(f"WARNING: Overwriting info for {nickname}")
    json_data[nickname] = {
        "local_user": local_user,
        "local_port": local_port,
    }
    json_data["_tb_executable"] = tb_executable
    with open(JSON_FILE, "w") as f:
        json.dump(json_data, f, indent=4, sort_keys=True)
    print(
        f"File {JSON_FILE} updated!\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"PLEASE RUN: ssh-copy-id -p {local_port} {local_user}@localhost\n"
        "to enable port forwarding to local machine via pubkey auth.\n"
        "(it will skip copying if key already exists on local machine.)\n"
        "If local machine is macOS, ENSURE THESE SETTINGS ARE SET:\n"
        "https://raw.githubusercontent.com/naokiyokoyama/my_env/main/imgs/mac_ssh.jpg\n"
        "Then run this script again.\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )
    exit()

# Load info about selected local machine
nickname = (
    json_data["_default_local_machine"] if args.nickname is None else args.nickname
)
local_user = json_data[nickname]["local_user"]
local_port = (
    json_data[nickname]["local_port"] if args.local_port is None else args.local_port
)
tb_executable = json_data["_tb_executable"]
print(
    f"tensorboard path: {tb_executable}\n"
    f"Selected local machine: {nickname}\n"
    f"Local port: {local_port}\nLocal username: {local_user}\n"
    f"FYI, you currently have these local machines registered: "
    f"{str([i for i in json_data.keys() if not i.startswith('_')])[1:-1]}\n"
    f"Run this script with --reconfigure to update above values."
)

# Find an available port to host the tensorboard
print("Searching for available port...")
viz_ports = list(range(8000, 9001))
random.seed(int(local_port))
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
        jobs_as_str = ["\n".join(existing_jobs)]
        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            "!!!!!!! WARNING !!!!!!!!!\n"
            "!!!!!!!!!!!!!!!!!!!!!!!!!\n"
            "You have existing tmux sessions created from this script:"
            f"{jobs_as_str}\n"
        )
except:
    pass

# Forward the tensorboard port back to local machine in the background
print("Connecting to local machine...")
tmux_session_name = f"rssh_{tb_port}"
cmd = (
    f"tmux new -s {tmux_session_name} -d "
    f"ssh -R {tb_port}:localhost:{tb_port} -p {local_port} {local_user}@localhost "
    '-o "StrictHostKeyChecking no"'
)
subprocess.check_call(cmd, shell=True)
print("Executed:\n", cmd, "\n")

# Now that ports are connected, run tensorboard.
print(f"Tensorboard will soon be available locally at: http://localhost:{tb_port}/")
print("Running tensorboard...\n")
try:
    # Run tensorboard command
    cmd = f"{tb_executable}  --port {tb_port} --logdir {args.logdir}"
    print("Executing:\n", cmd)
    subprocess.check_call(cmd, shell=True)
finally:
    # Kill the tmux session if user kill this python script
    cmd = f"tmux kill-session -t {tmux_session_name}"
    print("\nExecuting:\n", cmd)
    subprocess.check_call(cmd, shell=True)
    print("Successfully killed rssh tmux! Have a good day.")
