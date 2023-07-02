import argparse
import subprocess


def execute_command(cmd, args_list):
    """
    Executes the command with the given arguments.

    Args:
        cmd (str): The command string to execute.
        args_list (list): The arguments to pass to the command.

    Returns:
        int: The return code of the executed command.
    """
    command = cmd.format(*args_list)
    return subprocess.call(command, shell=True)


def iterate_commands(file_path, cmd):
    """
    Iterates through each line in the file, splits the line using '|', and executes the
    command with the splitted
    elements as arguments.

    Args:
        file_path (str): The path to the input file.
        cmd (str): The command string to execute.

    Returns:
        None
    """
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                args = line.split("|")
                assert cmd.count("{}") == len(
                    args
                ), "Number of '{}' placeholders and splitted elements are not the same."
                execute_command(cmd, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Iterate commands from a file")
    parser.add_argument("file_path", help="Path to the input file")
    parser.add_argument(
        "command",
        help="Command string to execute (use '{}' as a placeholder for the arguments)",
    )
    args = parser.parse_args()

    iterate_commands(args.file_path, args.command)
