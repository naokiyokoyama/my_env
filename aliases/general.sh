# Remove hostname from command line prompt prefix, just use username.
# Username will appear cyan in color. Conda env prefix recovered by env re-activation.
#PS1='\[\e[1;36m\]\u:\[\e[1;34m\]\w\[\e[0m\]$ '
#if [ ! -z "$CONDA_DEFAULT_ENV" ]
#then
#      conda activate $CONDA_DEFAULT_ENV
#fi

# set a fancy prompt (non-color, unless we know we "want" color); explicitly includes tmux sessions
case "$TERM" in
    xterm-color*|*-256color|screen*|tmux*) color_prompt=yes;;
esac

# General
alias sba='source ~/.bash_aliases'
alias eba='vim ~/.bash_aliases'
alias essh='vim ~/.ssh/config'
alias rp='realpath'
alias rmrf='rm -rf'
alias sl='ls'  # I always misspell this, so...
alias ls='ls --color=auto'
alias p9f='pkill -9 -f'

lnrp() {
  ln -s "$(realpath "$1")" "$2"
}

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
alias tmuxl='tmux ls'
alias tmux_rename='tmux rename-session -t'

tmuxa() {
  # If a session name is provided, attach to that session
  if [ -n "$1" ]; then
    tmux attach -t "$1"
    return
  fi

  # Count the number of running sessions
  local session_count=$(tmux ls 2>/dev/null | wc -l)

  # If there's exactly one session, attach to it
  if [ "$session_count" -eq 1 ]; then
    tmux attach
  elif [ "$session_count" -eq 0 ]; then
    echo "No tmux sessions running"
  else
    echo "Multiple sessions running. Please specify one:"
    tmux ls
  fi
}

tmuxk() {  # Provide one or more session names to kill
  for session_name in "$@"; do
    tmux kill-session -t "$session_name"
  done
}

tmuxk_glob() {  # e.g., tmuxk_glob "*mysession*"
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

tmux_interrupt() {  # Send Ctrl + C to a tmux. Good for timed self-destruction.
    if [ -z "$1" ]; then
        echo "Usage: tmux_interrupt <session_name>"
        return 1
    fi
    tmux send-keys -t "$1" C-c
}

tmux_run() {  # Sends a command to for a given session to run. Good for automated execution.
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: tmux_run <session_name> <command>"
        return 1
    fi
    tmux send-keys -t "$1" "$2" Enter
}

tmux_enter() {  # Sends an Enter key to a given tmux session
    if [ -z "$1" ]; then
        echo "Usage: tmux_enter <session_name>"
        return 1
    fi
    tmux send-keys -t "$1" Enter
}

# Other
alias tb='tensorboard --logdir'

wait_for_output() {
    # Function to wait until a command's output contains a specific string
    # Usage: wait_for_output "command" "expected_string"
    
    # Example usage:
    # wait_for_output "docker ps" "healthy"
    # wait_for_output "curl http://localhost:8080/health" "ready"
    
    local command="$1"
    local expected="$2"
    local interval=2   # Check interval: 2 seconds
    local start_time=$(date +%s)
    
    if [[ -z "$command" || -z "$expected" ]]; then
        echo "Error: Both command and expected string are required" >&2
        echo "Usage: wait_for_output \"command\" \"expected_string\"" >&2
        return 1
    fi
    
    echo "Waiting for output containing: $expected"
    echo "Command: $command"
    
    while true; do
        # Run the command and capture its output
        local output
        output=$(eval "$command" 2>&1)
        local exit_code=$?
        
        # Check if the command failed
        if [[ $exit_code -ne 0 ]]; then
            echo "Error: Command failed with exit code $exit_code" >&2
            echo "Command output: $output" >&2
            return $exit_code
        fi
        
        # Check if the expected string is in the output
        if echo "$output" | grep -q "$expected"; then
            echo "Found expected output!"
            echo "$output"
            return 0
        fi
        
        sleep "$interval"
    done
}

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
pbcatn() {
  # Group the commands so their combined output is piped to pbcopy
  {
    # 1. Get the basename of the file, add a colon, and print a newline
    basename "$1" | tr -d '\n' # Get basename and remove its trailing newline
    echo ":"                    # Print the colon and a final newline
    
    # 2. Catenate the actual file content
    cat "$1"
  } | pbcopy
}
pbwhich() {
  which $1 | pbcopy
}
pbls () {
  ls $1 | pbcopy
}
peeb() {
  echo $1 | pbcopy
}
pt() {  # for pasting to a file
    if [ $# -eq 0 ]; then
        echo "Usage: pt <filepath>"
        return 1
    fi
    
    filepath="$1"
    cat > "$filepath"
}

. $MY_ENV_REPO/my_useful/z.sh
