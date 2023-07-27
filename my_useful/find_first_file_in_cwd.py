import os
import fnmatch
import argparse
from typing import Optional

ALIAS = "ffind"


def find_first_match(pattern: str, path: str) -> Optional[str]:
    """
    Function to find the first file that matches a given pattern.

    Args:
        pattern (str): The pattern to match.
        path (str): The path to search in.

    Returns:
        str: The path of the first file that matches the pattern, or None if no match is found.
    """
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the first file that matches a given pattern."
    )
    parser.add_argument("pattern", type=str, help="The pattern to match.")
    parser.add_argument("path", type=str, help="The path to search in.")
    args = parser.parse_args()

    # usage
    match = find_first_match(args.pattern, args.path)
    if match:
        print(f"First match: {match}")
    else:
        print("No match found")
