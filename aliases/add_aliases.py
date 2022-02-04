import glob
import os
import os.path as osp
import subprocess
from sys import platform

operating_systems = {
    "linux": "ubuntu",
    "darwin": "macOS",
}
assert platform in operating_systems, "Can't determine operating system!"

op_sys = operating_systems[platform]
print("Detected operating system:", op_sys)
if input("Is this correct? [y/n]: ") != "y":
    print("Aborting.")
    exit()

header = "# >>> BEGINNING OF THINGS ADDED BY my_env REPO>>>\n"
footer = "\n# <<< END OF THINGS ADDED BY my_env REPO<<<\n"

# Erase existing block generated by this script if it exists
home_dir = osp.join(os.environ["HOME"])
local_aliases_file = osp.join(home_dir, ".bash_aliases")
if osp.isfile(local_aliases_file):
    with open(local_aliases_file) as f:
        data = f.read()
    if data.count(header) == 1 and data.count(footer) == 1:
        data = data.split(header)[0] + data.split(footer)[-1]
        print(
            "Erasing old block generated previously by this script from "
            f"{local_aliases_file}..."
        )
        with open(local_aliases_file, "w") as f:
            f.write(data)

added_aliases = header
this_dir = osp.dirname(osp.abspath(__file__))

# Add general aliases first
general_aliases = osp.join(this_dir, "general.sh")
with open(general_aliases) as f:
    added_aliases += f.read() + "\n"
print(f"Loading general aliases from '{general_aliases}'..")

# Add OS-specific aliases
if op_sys == "ubuntu":
    os_aliases = osp.join(this_dir, "ubuntu.sh")
else:  # macOS
    os_aliases = osp.join(this_dir, "macos.sh")
    # Add command to source ~/.bash_aliases if it doesn't exist yet
    bash_profile = osp.join(home_dir, ".bash_profile")
    if osp.isfile(bash_profile):
        with open(bash_profile) as f:
            data = f.read()
    else:
        data = ""
    src_alias_cmd = "source ~/.bash_aliases"
    if src_alias_cmd not in data:
        with open(bash_profile, "a+") as f:
            f.write(data + "\n" + src_alias_cmd + "\n")
        print(f"Wrote '{src_alias_cmd}' to {bash_profile}, b/c it wasn't there before.")

# Load OS-specific aliases from this repo
with open(os_aliases) as f:
    added_aliases += f.read() + "\n"
print(f"Loading OS-specific aliases from '{os_aliases}'..")

# Replace environment variable with valid path to this repo
my_env_repo = osp.dirname(this_dir)
added_aliases = added_aliases.replace("<MY_ENV_REPO>", my_env_repo)
added_aliases += footer

# Prepend added aliases to existing ones, if there are existing ones
if osp.isfile(local_aliases_file):
    with open(local_aliases_file) as f:
        added_aliases += f.read()
with open(local_aliases_file, "w") as f:
    f.write(added_aliases)

print(f"Successfully pre-pended all aliases to '{local_aliases_file}'!")

bin_dir = osp.join(my_env_repo, "bin")
for exe in glob.glob(osp.join(bin_dir, "*")):
    subprocess.check_call(f"chmod +x {exe}".split())
print(f"Successfully made all scripts in '{bin_dir}' executable! Added to PATH.")
