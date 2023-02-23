"""
Connects an available port to your local machine and then runs tensorboard on that
port.
"""
ALIAS = "tbr"

import argparse
import json
import os
import os.path as osp
import random
import shutil
import socket
import subprocess

JSON_FILE = osp.abspath(__file__).replace(".py", ".json")


def main(logdir, reconfigure, local_port, nickname, tmp_dir):
    if osp.isfile(JSON_FILE):
        with open(JSON_FILE) as f:
            json_data = json.load(f)
    else:
        json_data = None

    if tmp_dir is None:
        logdir = logdir[0]
    else:
        # Generate a symlink for each logdir in tmp_dir
        symlinks = shorten_paths(
            [dirname.lstrip("/").rstrip("/") for dirname in logdir]
        )
        for dirname, symlink in zip(logdir, symlinks):
            symlink = osp.join(tmp_dir, symlink)
            if "/" in symlink:
                os.makedirs(osp.dirname(symlink), exist_ok=True)
            os.symlink(osp.abspath(dirname), symlink)
        logdir = tmp_dir

    if json_data is None or reconfigure:
        configure(json_data)
        exit()

    # Load info about selected local machine
    nickname = json_data["_default_local_machine"] if nickname is None else nickname
    local_user = json_data[nickname]["local_user"]
    local_port = json_data[nickname]["local_port"] if local_port is None else local_port
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
        existing_jobs = [
            line.split(":")[0] for line in out.splitlines() if "rssh_" in line
        ]
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
        cmd = f"{tb_executable}  --port {tb_port} --logdir {logdir}"
        print("Executing:\n", cmd)
        subprocess.check_call(cmd, shell=True)
    finally:
        # Kill the tmux session if user kill this python script
        cmd = f"tmux kill-session -t {tmux_session_name}"
        print("\nExecuting:\n", cmd)
        subprocess.check_call(cmd, shell=True)
        print("Successfully killed rssh tmux! Have a good day.")


def configure(json_data):
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
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        f"PLEASE RUN: ssh-copy-id -p {local_port} {local_user}@localhost\n"
        "to enable port forwarding to local machine via pubkey auth.\n"
        "(it will skip copying if key already exists on local machine.)\n"
        "If local machine is macOS, ENSURE THESE SETTINGS ARE SET:\n"
        "https://raw.githubusercontent.com/naokiyokoyama/my_env/main/imgs/mac_ssh.jpg\n"
        "Then run this script again.\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"
    )


def shorten_paths(path_list):
    def all_lists_longer_than_1(list_of_lists):
        return all([len(l) > 1 for l in list_of_lists])

    def filter_list_of_lists(list_of_lists):
        while all_lists_longer_than_1(list_of_lists):
            for split_path in list_of_lists[1:]:
                if list_of_lists[0][0] != split_path[0]:
                    return list_of_lists
            for i in range(len(list_of_lists)):
                list_of_lists[i] = list_of_lists[i][1:]

    path_list_list = filter_list_of_lists([path.split("/") for path in path_list])
    new_path_list = ["/".join(path) for path in path_list_list]
    return new_path_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Add an argument called logdir that is a list of paths, with at least one path
    parser.add_argument("logdir", nargs="+", help="Path(s) to logdir(s)")
    parser.add_argument(
        "-r",
        "--reconfigure",
        action="store_true",
        help="Use this flag to update info about local machines",
    )
    parser.add_argument(
        "-l",
        "--local_port",
        type=int,
        help="Override port to connect to on local machine in case RemoteForward fails",
    )
    parser.add_argument(
        "-n",
        "--nickname",
        help="Which local machine to connect to",
    )
    args = parser.parse_args()

    # Create a temporary dir if multiple logdirs are passed
    if len(args.logdir) > 1:
        # Create a temp dir to store symlinks to all log_dirs
        tmp_dir = f"/tmp/tb_{random.randint(0, 9999)}"
        while osp.isdir(tmp_dir):
            tmp_dir = f"/tmp/tb_{random.randint(0, 9999)}"
        os.mkdir(tmp_dir)
    else:
        tmp_dir = None

    try:
        main(args.logdir, args.reconfigure, args.local_port, args.nickname, tmp_dir)
    finally:
        if tmp_dir is not None:
            shutil.rmtree(tmp_dir)
