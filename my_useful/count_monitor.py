import argparse
import subprocess
import time


def run_command(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, error = process.communicate()
    return output.decode("utf-8").strip()


def count_lines(output):
    return len(output.splitlines())


def main():
    parser = argparse.ArgumentParser(
        description="""
        Monitor the line count of a command's output and exit based on specified
        conditions.

        This script repeatedly runs a given command at specified intervals, counts
        the lines of its output, and exits when certain conditions are met. It can
        be used to monitor file counts, log entries, or any other scenario where you
        need to track the number of lines in a command's output over time.

        The script can exit when the line count equals, exceeds, or falls below a
        specified target, depending on the flags used. It also provides options to
        customize the check interval and enable debug output.

        Examples:
        1. Exit when line count equals 10:
           python count_monitor.py 'ls /path/to/dir' 10

        2. Exit when line count is less than 5:
           python count_monitor.py -l 'ls /path/to/dir' 5

        3. Exit when line count exceeds 20, checking every 10 seconds:
           python count_monitor.py -g -s 10 'ls /path/to/dir' 20

        4. Monitor with debug output:
           python count_monitor.py -d 'ls /path/to/dir | grep pattern' 15
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", help="Command to run (in quotes)")
    parser.add_argument("target_count", type=int, help="Target line count")
    parser.add_argument(
        "-l", "--less", action="store_true", help="Exit when count is less than target"
    )
    parser.add_argument(
        "-g",
        "--greater",
        action="store_true",
        help="Exit when count is greater than target",
    )
    parser.add_argument(
        "-s",
        "--sleep",
        type=int,
        default=5,
        help="Sleep time between checks (in seconds)",
    )

    args = parser.parse_args()

    assert not (
        args.less and args.greater
    ), "Cannot use both -l and -g flags simultaneously"

    print(f"Monitoring command: {args.command}")
    print(f"Target line count: {args.target_count}")
    print(f"Sleep time: {args.sleep} seconds")

    while True:
        output = run_command(args.command)
        current_count = count_lines(output)

        print(f"Current line count: {current_count}")

        if args.less and current_count < args.target_count:
            print("Count is less than target. Exiting.")
            break
        elif args.greater and current_count > args.target_count:
            print("Count is greater than target. Exiting.")
            break
        elif not (args.less or args.greater) and current_count == args.target_count:
            print("Target count reached!")
            break

        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
