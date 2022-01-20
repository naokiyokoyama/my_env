import os
import os.path as osp
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

added_aliases = "\n# >>> BEGINNING OF THINGS ADDED BY my_env REPO>>>\n"
this_dir = osp.dirname(osp.abspath(__file__))

# Add general aliases first
general_aliases = osp.join(this_dir, "general.sh")
with open(general_aliases) as f:
    added_aliases += f.read() + "\n"
print(f"Loading general aliases from '{general_aliases}'..")

# Add OS-specific aliases
home_dir = osp.join(os.environ["HOME"])
if op_sys == "ubuntu":
    os_alias_file = "ubuntu.sh"
else:  # macOS
    os_alias_file = "macos.sh"
    # Add command to source ~/.bash_aliases if it doesn't exist yet
    bash_profile = osp.join(home_dir, ".bash_profile")
    with open(bash_profile) as f:
        data = f.read()
    src_alias_cmd = "source ~/.bash_aliases"
    if src_alias_cmd not in data:
        with open(bash_profile, "a") as f:
            f.write(data + "\n" + src_alias_cmd + "\n")
        print(f"Wrote '{src_alias_cmd}' to {bash_profile}, b/c it wasn't there before.")

# Load OS-specific aliases from this repo
os_aliases = osp.join(this_dir, os_alias_file)
with open(os_aliases) as f:
    added_aliases += f.read() + "\n"
print(f"Loading OS-specific aliases from '{os_aliases}'..")

# Replace environment variable with valid path to this repo
useful_dir = osp.dirname(this_dir)
added_aliases = added_aliases.replace("<MY_USEFUL_SCRIPTS_DIR>", useful_dir)
added_aliases += "\n# <<< END OF THINGS ADDED BY my_env REPO<<<\n"

local_aliases_file = osp.join(home_dir, ".bash_aliases")
with open(local_aliases_file, "a") as f:
    f.write(added_aliases)

print(f"Successfully added all aliases to '{local_aliases_file}'!")
