"""
Stitches images in folder into video, by filename (alphabetically)
"""

import argparse
import glob
import os.path as osp

import tqdm
from moviepy.editor import ImageClip, concatenate_videoclips

IMAGE_EXTS = ["png", "jpg"]

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="path to folder containing images")
parser.add_argument("-f", "--fps", default=30, type=float, help="output video fps")
args = parser.parse_args()

# Get all the image files in the directory
all_files = glob.glob(osp.join(args.folder, "*"))
all_imgs = sorted([i for i in all_files if i.lower().split(".")[-1] in IMAGE_EXTS])
print(f"Found {len(all_imgs)} image files")

print(f"Converting images into clips")
clips = [ImageClip(m).set_duration(1 / args.fps) for m in tqdm.tqdm(all_imgs)]

basename = osp.basename(osp.abspath(args.folder))
concat_clip = concatenate_videoclips(clips, method="compose")
out_path = osp.join(args.folder, basename + ".mp4")
concat_clip.write_videofile(out_path, fps=args.fps)
print(f"Saved video to {out_path}!")
