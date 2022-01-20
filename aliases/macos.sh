# Remove "pLz UpGrAdE tO zSh" message because we're using bash
export BASH_SILENCE_DEPRECATION_WARNING=1

# Make history store only unique commands
export HISTCONTROL=ignoredups

# Re-source the bash_profile
alias sbr='source ~/.bash_profile'

# HEIC to JPG file converter. Example: h2j *.HEIC
alias h2j='magick mogrify -monitor -format jpg'

# Print absolute file path of input filename
realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

# Enable glob negation
shopt -s extglob
