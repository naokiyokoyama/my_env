# my_env
Convenient scripts and configuration files meant for quick setup on a new machine.
## How to add aliases
This script will pre-pend a block of code to your existing `~/.bash_aliases` file to define new aliases without overwriting existing ones. It will create this file if it doesn't exist, and for macOS, will make `~/.bash_profile` source it if it doesn't already do so. 
```python
python aliases/add_aliases.py
```
## Useful scripts
Use the `-h` flag to learn about what args each script needs.
- `replace_all_in_file.py` - can be called using `repall` alias added by this repo. Given a file, replaces all occurrences of `str1` with `str2`.
- `default_scp.py` - can be called using `dscp` alias added by this repo. Executes `scp` command on using your favorite remote host so you don't have to keep writing it out (must export `$DEFAULT_REMOTE_HOST`). 
- `video2gif.py` - converts video to gif (useful for Google Slides)
- `speedup_video.py` - creates faster copy of video (removes sound)
- `count.py` - just prints out numbers from `int1` to `int2` each on a new line (OK not too useful, but sometimes useful when composing repetitive commands in a text editor) 
