import argparse
import os.path as osp

from moviepy.editor import VideoFileClip

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--fps", type=float, default=30)
parser.add_argument("--out-path")
args = parser.parse_args()

if args.out_path is None:
    args.out_path = osp.join(
        osp.dirname(osp.abspath(args.file)),
        f"fps_{args.fps}_" + osp.basename(args.file),
    )

# loading video dsa gfg intro video
clip = VideoFileClip(args.file)
clip.write_videofile(args.out_path, fps=args.fps)
