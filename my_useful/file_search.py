import argparse
import os.path as osp
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("query")
parser.add_argument("files", nargs="+")
parser.add_argument("-B", "--before", default=0, type=int)
parser.add_argument("-A", "--after", default=0, type=int)
args = parser.parse_args()

for i in args.files:
    if not osp.isfile(i):
        print(f"{i} is not a file! Skipping")
        continue

    with open(i) as f:
        data = f.read()

    if args.query in data:
        print(i + ":")
        subprocess.check_call(
            f"cat {i} | grep -B {args.before} -A {args.after} '{args.query}'",
            shell=True,
        )
