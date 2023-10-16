alias sq='squeue -u $USER --sort=P,i,t,+j --format "%.12i %.9P %.45j %.2t %.10M %R"'
scan() {
    # Cancels the given job ids and removes the corresponding .slurm_job files,
    # if they exist.
    # Don't worry if you don't have the directory '~/slurm_poll_stuck_jobs'
    #
    # Usage:
    #   scan <jobid1> <jobid2> ...
    # Example:
    #   scan 1234 5678 91011

    # First, run scancel for each argument
    scancel "$@"

    # Then, remove the corresponding .slurm_job files from the directory
    for jobid in "$@"; do
        rm -f ~/slurm_poll_stuck_jobs/${jobid}.slurm_job
    done
}

# Supposed to stand for "scancel range". Given two job_ids, it will try to cancel
# both job_ids and all ids in between.
rscan() {
  python -c "import os; os.system('scancel ' + ' '.join([str(i) for i in range($1, $2+1)]))"
}

alias sbam='python $MY_ENV_REPO/slurm/sbatch_glob.py'
alias sbarg='python $MY_ENV_REPO/slurm/sbatch_with_args.py'
alias sbash='python $MY_ENV_REPO/slurm/slurm_interactive_bash.py'
cd_sbatch () {
  cd $(dirname $1) # cd into the parent dir of $1 file path
  sbatch $(basename $1)
  cd - # go back to the original dir
}
sbase() {
  # Change job name to the basename of the current directory
  base=$(basename $PWD)
  sbatch --job-name $base $1
}
cd_sbase() {
  # Change job name to the basename of the current directory
  base=$(basename $PWD)
  cd $(dirname $1) # cd into the parent dir of $1 file path
  sbatch --job-name $base $1
  cd - # go back to the original dir
}
