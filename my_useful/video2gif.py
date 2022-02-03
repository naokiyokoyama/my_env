"""
Why doesn't Google Slides accept .mp4 files, huh?
"""
import argparse
import os.path as osp

from moviepy.editor import VideoFileClip

parser = argparse.ArgumentParser()
parser.add_argument("video_path")
parser.add_argument(
    "-o", "--out_path", help="defaults to orig path but with .gif extension"
)
parser.add_argument("-m", "--max_height", default=256, type=int, help="default: 256")
parser.add_argument("--fps", type=int, default=10)
args = parser.parse_args()

if args.out_path is None:
    basename = osp.basename(args.video_path)
    new_basename = osp.splitext(basename)[0] + ".gif"
    args.out_path = args.video_path.replace(basename, new_basename)

clip = VideoFileClip(args.video_path)

# Don't upscale the video
args.max_height = min(args.max_height, clip.h)

scale = args.max_height / clip.h
print(f"Original dimensions: {clip.w} x {clip.h}")
print(f"New dimensions: {int(clip.w * scale)} x {int(clip.h * scale)}")

clip = clip.resize(scale)
clip.write_gif(args.out_path, fps=args.fps)
