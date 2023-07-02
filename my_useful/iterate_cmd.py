import argparse
import subprocess
from typing import List


def execute_command(cmd: str, args_list: List[str], silent=False) -> None:
    """
    Executes the command with the given arguments.

    Args:
        cmd (str): The command string to execute.
        args_list (List[str]): The arguments to pass to the command.
        silent (bool): Whether to print the command or not. Defaults to False.
    Returns:
        None
    """
    if not silent:
        print(args_list)
    command = cmd.format(*args_list)
    subprocess.check_call(command, shell=True)


def iterate_commands(file_path: str, cmd: str, silent: bool = False) -> None:
    """
    Iterates through each line in the file, splits the line using '|', and executes the
    command with the split elements as arguments.

    Args:
        file_path (str): The path to the input file.
        cmd (str): The command string to execute.
        silent (bool): Whether to print the command or not. Defaults to False.
    Returns:
        None
    """
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  # Skip lines that start with '#'
                args = line.split("|")
                assert cmd.count("{}") == len(
                    args
                ), "Number of '{}' placeholders and splitted elements are not the same."
                execute_command(cmd, args, silent=silent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Iterate commands from a file")
    parser.add_argument("file_path", help="Path to the input file")
    parser.add_argument(
        "command",
        help="Command string to execute (use '{}' as a placeholder for the arguments)",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Whether to print the args to the command or not",
    )
    args = parser.parse_args()

    iterate_commands(args.file_path, args.command, silent=args.silent)
