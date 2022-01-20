import sys
import subprocess

cmd = " && \\\n".join([f"sbatch {i}" for i in sys.argv[1:]])
print(cmd)

if input('\nExecute? Enter "y" for yes: ') == "y":
    print("Executing...")
    subprocess.check_call(cmd, shell=True)
else:
    print("Aborting.")
