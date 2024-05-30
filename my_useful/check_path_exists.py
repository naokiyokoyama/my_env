import os
import argparse
import time

def check_path_exists(path):
    while not os.path.exists(path):
        print(f"Waiting for '{path}' to exist...")
        time.sleep(1)
    print(f"'{path}' exists!")

def main():
    parser = argparse.ArgumentParser(description="Check if a file, directory, or symlink exists.")
    parser.add_argument("path", help="Path to the file, directory, or symlink")
    args = parser.parse_args()

    check_path_exists(args.path)

if __name__ == "__main__":
    main()
