"""
Meant for use in skynet. You would have to change partition names for other
SLURM clusters.
"""

import os
import sys
from typing import Any


def get_arg(args: list, choices: list, default: Any):
    for i in choices:
        if i in args:
            # Return all the other args
            remaining = args[: args.index(i)] + args[args.index(i) + 2 :]
            return args[args.index(i) + 1], remaining
    return default, args


def print_help():
    print(
        "Usage: python slurm_interactive_bash.py [options]"
        "Some helpful options:"
        "  -c, --cpus-per-task: number of cpus per task (default: 6)"
        "  -J, --job-name: name of the job (default: bash)"
        "  -C, --constraint: type of gpu (default: any)"
        "  -p, --partition: partition to use (default: debug)"
        "  -x, --exclude: nodes to avoid (default: $BLACKLIST_NODES)"
    )
    exit(0)


def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print_help()
    num_cpus, args = get_arg(args, ["-c", "--cpus-per-task"], 6)
    job_name, args = get_arg(args, ["-J", "--job-name"], "bash")
    partition, args = get_arg(args, ["-p", "--partition"], "debug")
    exclude_nodes, args = get_arg(args, ["-x", "--exclude"], "")
    exclude_nodes = exclude_nodes.split(",") + os.environ.get(
        "BLACK_LIST_NODES", ""
    ).split(",")
    exclude_nodes = ",".join(exclude_nodes)

    cmd = (
        "srun --gres gpu:1 --nodes 1"
        f" --cpus-per-task {num_cpus}"
        f" --job-name {job_name}"
        f" --partition {partition}"
        f" --exclude {exclude_nodes}"
        f" {' '.join(args)}"
        " --pty bash"
    )
    print("Executing:")
    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    main()
