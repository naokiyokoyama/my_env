# Remove hostname from command line prompt prefix, just use username.
# Username will appear cyan in color. This interferes with conda if called
# afterward though, need to add logic to fix.
#PS1='\[\e[1;36m\]\u:\[\e[1;34m\]\w\[\e[0m\]$ '

# General
alias sba='source ~/.bash_aliases'
alias eba='vim ~/.bash_aliases'
alias essh='vim ~/.ssh/config'
alias rp='realpath'
alias sl='ls'  # I always misspell this, so...
alias ls='ls --color=auto'
alias l='ls -CF'

# Conda
alias ca='conda activate'
alias condad='conda deactivate'
alias condac='conda create -n '

# Git
alias gita='git add'
alias gitc='git commit -m'
alias gitp='git push'
alias gits='git status'
alias gitd='git diff'

# tmux
alias tmuxs='tmux new -s'
alias tmuxa='tmux a -t'
alias tmuxl='tmux ls'
alias tmuxk='tmux kill-session -t'

# my_useful scripts
export DEFAULT_REMOTE_HOST=''
export MY_ENV_REPO='<MY_ENV_REPO>'  # filled in by add_aliases.py
alias dscp='python $MY_ENV_REPO/my_useful/default_scp.py'
alias countint='python $MY_ENV_REPO/my_useful/count.py'
alias repall='python $MY_ENV_REPO/my_useful/replace_all_in_file.py'
alias cpwd="pwd | pbcopy && echo 'Copied:' `pwd`"
cprp() {
    realpath $1 | pbcopy && echo 'Copied:' `realpath $1`
}
