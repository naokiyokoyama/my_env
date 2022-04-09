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
alias ca='conda activate'
alias condad='conda deactivate'
alias mambac='conda create -n '

# Git
alias gita='git add'
alias gitc='git commit -m'
alias gitp='git push'
alias gits='git status'
alias gitd='git diff'

# tmux
alias tmuxs='tmux new -s'
alias tmuxa='tmux attach -t'
alias tmuxl='tmux ls'
alias tmuxk='tmux kill-session -t'
alias tmux_rename='tmux rename-session -t'

# Other
alias tb='tensorboard --logdir'

# my_useful scripts
export DEFAULT_REMOTE_HOST='<DEFAULT_REMOTE_HOST>'
export MY_ENV_REPO='<MY_ENV_REPO>'  # filled in by add_aliases.py
export PATH="$MY_ENV_REPO/bin:$PATH"
alias cpwd="pwd | pbcopy && echo 'Copied:' `pwd`"
alias pull_my_env='git -C $MY_ENV_REPO pull'
alias regenerate_executables="python $MY_ENV_REPO/aliases/generate_executables.py"
cprp() {
    realpath $1 | pbcopy && echo 'Copied:' `realpath $1`
}
. $MY_ENV_REPO/my_useful/z.sh
