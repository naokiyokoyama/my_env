import subprocess
import argparse
import os

copy_cmd = (
    "rsync -rav --progress -e "
    "'ssh -T -c chacha20-poly1305@openssh.com -o Compression=no -x' "
    "{exclude} {src} {dst}"
)


def main(src, dst, exclude):
    if ":" not in src:
        host = os.environ.get("DEFAULT_REMOTE_HOST", "")
        assert host != "", "Default host ($DEFAULT_REMOTE_HOST) has not been set!"
        src = f"{host}:" + src
    if exclude != "":
        exclude = "--exclude=" + exclude.replace(",", " --exclude=")
    cmd = copy_cmd.format(exclude=exclude, src=src, dst=dst)
    print(f"Executing:\n{cmd}")
    subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dst", nargs="?", default=os.getcwd())
    parser.add_argument("-x", "--exclude", default="")
    args = parser.parse_args()
    main(args.src, args.dst, args.exclude)
