import argparse
import glob
import time

parser = argparse.ArgumentParser()
parser.add_argument("glob_string")
parser.add_argument("count", type=int)
args = parser.parse_args()

assert "*" in args.glob_string

count = len(glob.glob(args.glob_string))
while count < args.count:
    count = len(glob.glob(args.glob_string))
    print("Current count:", count)
    time.sleep(10)
