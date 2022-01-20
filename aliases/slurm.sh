alias sq='squeue -u $USER --sort=P,i,t,+j --format "%.12i %.9P %.45j %.2t %.10M %R"'
alias scan='scancel'

# Supposed to stand for "scancel range"
rscan() {
  python -c "import os; os.system('scancel ' + ' '.join([str(i) for i in range($1, $2+1)]))"
}

alias sbam='python $MY_USEFUL_SCRIPTS_DIR/sbatch_glob.py'
alias sbarg='python $MY_USEFUL_SCRIPTS_DIR/sbatch_with_args.py'
