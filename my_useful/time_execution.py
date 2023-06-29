import argparse
import subprocess
import time


def time_bash_command(command):
    start_time = time.time()
    process = subprocess.Popen(command, shell=True)
    process.wait()
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Time the execution of a bash command")
    parser.add_argument("command", type=str, help="The bash command to execute")
    args = parser.parse_args()

    execution_time = time_bash_command(args.command)
    print(f"Execution time: {execution_time} seconds")
