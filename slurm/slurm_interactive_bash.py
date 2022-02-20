"""
Meant for use in skynet. You would have to change partition names for other
SLURM clusters.
"""

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--job_name", default="bash", help="name to give job")
parser.add_argument(
    "-c",
    "--num_cpus",
    type=int,
    default=6,
    help="number of cpus to allocate to the job",
)
parser.add_argument(
    "-x",
    "--exclude",
    help="list of nodes to avoid, separated by commas",
)
parser.add_argument(
    "-w",
    "--want",
    default="",
    help="name of node that you want to run the job on",
)
parser.add_argument(
    "-p", "--partition", type=str, default="short", help="partition to run the job on"
)
parser.add_argument(
    "-u",
    "--user-overcap",
    action="store_true",
    help="indicates submission to user-overcap partition",
)
parser.add_argument(
    "-o",
    "--overcap",
    action="store_true",
    help="indicates submission to overcap partition",
)
parser.add_argument(
    "-q",
    "--quadro",
    action="store_true",
    help="indicates desire to use a node with Quadro cards",
)
args = parser.parse_args()

cmd = (
    "srun --gres gpu:1 --nodes 1"
    f" --cpus-per-task {args.num_cpus}"
    f" --job-name {args.job_name}"
)

# Node to exclude
exclude_nodes = os.environ.get("BLACK_LIST_NODES", "").split(",")
if args.exclude is not None:
    exclude_nodes.extend(args.exclude.split(","))
if len(exclude_nodes) > 0:
    cmd += f" --exclude {','.join(exclude_nodes)}"

# Which slurm partition to use
if args.overcap:
    cmd += " --account overcap --partition overcap"
elif args.user_overcap:
    cmd += " --partition user-overcap"
else:
    cmd += f" --partition {args.partition}"

if args.want != "":
    cmd += f" -w {args.want}"

if args.quadro:
    cmd += f" --constraint claptrap,glados,olivaw,oppy,sophon,zima"

cmd += " --pty bash"

print("Executing: ", cmd)
os.system(cmd)
