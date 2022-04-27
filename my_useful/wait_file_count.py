import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("glob_string")
parser.add_argument("count")
args = parser.parse_args()

assert "*" in args.glob_string

subprocess.check_call(
    f"files=( {args.glob_string} );"
    "$num_files=${#files[@]};"
    f"while [ $num_files -lt {args.count} ]; do sleep 10;"
    f"files=( {args.glob_string} );"
    "$num_files=${#files[@]};"
    "echo $num_files files currently.;"
    "done"
)
