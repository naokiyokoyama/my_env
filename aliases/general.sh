# Remove hostname from command line prompt prefix, just use username.
# Username will appear cyan in color. Conda env prefix recovered by env re-activation.
#PS1='\[\e[1;36m\]\u:\[\e[1;34m\]\w\[\e[0m\]$ '
#if [ ! -z "$CONDA_DEFAULT_ENV" ]
#then
#      conda activate $CONDA_DEFAULT_ENV
#fi

# General
alias sba='source ~/.bash_aliases'
alias eba='vim ~/.bash_aliases'
alias essh='vim ~/.ssh/config'
alias rp='realpath'
alias rmrf='rm -rf'
alias sl='ls'  # I always misspell this, so...
lsgrep() {
  ls | grep $1
}
mkdircd() {
    mkdir $1 && cd $1
}

# Conda
ca() {
  if [ "$CONDA_DEFAULT_ENV" != "$1" ]; then
    conda activate "$1"
  else
    echo "Conda environment $1 is already active."
  fi
}
alias condad='conda deactivate'
alias mambac='conda create -n '

# Git
alias gita='git add'
alias gitc='git commit -m'
alias gitp='git push'
alias gits='git status'
alias gitd='git diff'
gpush() {
  git add -u && git commit -m "${1}" && git push
}
gstash_file() {
  # Assert two args were given
  if [ -z "$2" ]
  then
      echo "Please provide two args: file and message"
      return
  fi
  git stash push -m "${2}" ${1}
}

# tmux
alias tmuxs='tmux new -s'
alias tmuxa='tmux attach -t'
alias tmuxl='tmux ls'
alias tmux_rename='tmux rename-session -t'
tmuxk() {  # Provide one or more session names to kill
  for session_name in "$@"; do
    tmux kill-session -t "$session_name"
  done
}
tmuxk_wildcard() {  # e.g., kill_tmux_wildcard "*mysession*"
    local session_pattern=$1

    # Ensure that a pattern was provided
    if [[ -z "$session_pattern" ]]; then
        echo "Usage: $0 <session_pattern>"
        return 1
    fi

    # Get the list of all running tmux sessions
    local sessions=$(tmux ls -F "#{session_name}")

    # Iterate over the sessions and kill the ones that match the pattern
    for session in $sessions; do
        if [[ $session == $session_pattern ]]; then
            tmux kill-session -t "$session"
        fi
    done
}

# Other
alias tb='tensorboard --logdir'

# my_useful scripts
export DEFAULT_REMOTE_HOST='<DEFAULT_REMOTE_HOST>'
export MY_ENV_REPO='<MY_ENV_REPO>'  # filled in by add_aliases.py
export PATH="$MY_ENV_REPO/bin:$PATH"
alias cpwd="pwd | pbcopy && echo 'Copied:' `pwd`"
alias pull_my_env='git -C $MY_ENV_REPO pull'
alias regenerate_executables="python $MY_ENV_REPO/aliases/generate_executables.py"
alias tbr='python $MY_ENV_REPO/my_useful/remote_to_local_tensorboard.py'

# pbcopy aliases
cprp() {
  realpath $1 | pbcopy && echo 'Copied:' `realpath $1`
}
pbcat() {
  cat $1 | pbcopy
}
pbwhich() {
  which $1 | pbcopy
}
peeb() {
  echo $1 | pbcopy
}

. $MY_ENV_REPO/my_useful/z.sh
