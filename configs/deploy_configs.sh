#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Mapping: "repo_relative_path:target_path:filter_tag"
# filter_tag is used with --only to deploy a subset of configs
CONFIG_MAP=(
    ".tmux.conf:$HOME/.tmux.conf:tmux"
    ".vimrc:$HOME/.vimrc:vim"
    ".wezterm.lua:$HOME/.wezterm.lua:wezterm"
    "zellij/config.kdl:$HOME/.config/zellij/config.kdl:zellij"
    "zellij/layouts/quad.kdl:$HOME/.config/zellij/layouts/quad.kdl:zellij"
)

usage() {
    echo "Usage: $(basename "$0") [--only <tool>]"
    echo
    echo "Symlinks config files from this repo to their expected locations."
    echo
    echo "Options:"
    echo "  --only <tool>  Deploy only configs for a specific tool"
    echo "                 Available: tmux, vim, wezterm, zellij"
    echo
    echo "Examples:"
    echo "  $(basename "$0")              # deploy all configs"
    echo "  $(basename "$0") --only zellij  # deploy only zellij configs"
}

FILTER=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --only)
            FILTER="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

for entry in "${CONFIG_MAP[@]}"; do
    IFS=':' read -r repo_rel target tag <<< "$entry"

    # Apply filter if specified
    if [[ -n "$FILTER" && "$tag" != "$FILTER" ]]; then
        continue
    fi

    source_path="$SCRIPT_DIR/$repo_rel"

    # Verify source exists in repo
    if [[ ! -f "$source_path" ]]; then
        echo "SKIP  $repo_rel (not found in repo)"
        continue
    fi

    # If target is already the correct symlink, skip
    if [[ -L "$target" && "$(readlink "$target")" == "$source_path" ]]; then
        echo "OK    $target -> $source_path"
        continue
    fi

    # If target exists (file or wrong symlink), back it up
    if [[ -e "$target" || -L "$target" ]]; then
        backup="${target}.bak.$(date +%Y%m%d%H%M%S)"
        echo "BACK  $target -> $backup"
        mv "$target" "$backup"
    fi

    # Create parent directories if needed
    mkdir -p "$(dirname "$target")"

    # Create symlink
    ln -s "$source_path" "$target"
    echo "LINK  $target -> $source_path"
done
