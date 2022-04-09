ALIAS = "repall"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("str_to_replace")
parser.add_argument("str_to_replace_with")
args = parser.parse_args()

with open(args.file_path) as f:
    data = f.read()

occurrences = data.count(args.str_to_replace)
data = data.replace(args.str_to_replace, args.str_to_replace_with)

with open(args.file_path, "w") as f:
    f.write(data)

print(
    f"Replaced {occurrences} occurrences of {args.str_to_replace} "
    f"with {args.str_to_replace_with}."
)
