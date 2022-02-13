import subprocess
import sys


def main():
    slurm_files = sys.argv[1:]
    sbatch_all(slurm_files)


def sbatch_all(slurm_files):
    cmd = " && \\\n".join([f"sbatch {i}" for i in slurm_files])
    print(cmd)

    if input(f'\nSubmit {len(slurm_files)} jobs? Enter "y" for yes: ') == "y":
        print("Executing...")
        subprocess.check_call(cmd, shell=True)
    else:
        print("Aborting.")


if __name__ == "__main__":
    main()
