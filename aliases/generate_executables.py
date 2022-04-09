import glob
import os
import os.path as osp
import shutil
import subprocess

import tqdm


def generate_executables():
    python = osp.join(osp.dirname(os.environ["CONDA_EXE"]), "python")
    my_env_dir = osp.dirname(osp.dirname(osp.abspath(__file__)))
    scripts_dir = osp.join(my_env_dir, "my_useful")
    bin_dir = osp.join(my_env_dir, "bin")

    # Erase existing executables
    for i in glob.glob(osp.join(bin_dir, "*")):
        if "pbcopy" in i:
            continue
        os.remove(i)

    # Make all scripts executable
    scripts = glob.glob(osp.join(scripts_dir, "*.py"))
    # for script in scripts:
    for script in tqdm.tqdm(scripts):
        # Add executable path to the top of file
        with open(script) as f:
            data = f"#! {python}\n" + f.read()

        # Copy file over (w/o extension)
        if "ALIAS = " in data:
            bin_basename = data.split("ALIAS = ")[-1].split("\n")[0].replace('"', "")
        else:
            bin_basename = osp.basename(script)[:-3]
        bin_file = osp.join(bin_dir, bin_basename)
        shutil.copyfile(script, bin_file)
        with open(bin_file, "w") as f:
            f.write(data)

        cmd = f"chmod +x {bin_file}"
        subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    generate_executables()
