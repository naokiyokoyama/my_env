"""
Stitches images in folder into video, by filename (alphabetically)
"""

import argparse
import glob
import os.path as osp

import cv2
import tqdm

IMAGE_EXTS = ["png", "jpg"]

parser = argparse.ArgumentParser()
parser.add_argument("folder", help="path to folder containing images")
parser.add_argument("-f", "--fps", default=30, type=float, help="output video fps")
args = parser.parse_args()

# Get all the image files in the directory
all_files = glob.glob(osp.join(args.folder, "*"))


def sort_key(impath):
    base = osp.basename(impath)
    int_str = ""
    for i in base:
        if i.isdigit():
            int_str += i
        elif int_str != "":
            return int(int_str)


all_imgs = sorted(
    [i for i in all_files if i.lower().split(".")[-1] in IMAGE_EXTS], key=sort_key
)
print(f"Found {len(all_imgs)} image files")
basename = osp.basename(osp.abspath(args.folder))
out_path = osp.join(args.folder, basename + ".mp4")
out_vid = None
for impath in tqdm.tqdm(all_imgs):
    img = cv2.imread(impath)
    if out_vid is None:
        four_cc = cv2.VideoWriter_fourcc(*"MP4V")
        height, width = img.shape[:2]
        out_vid = cv2.VideoWriter(out_path, four_cc, args.fps, (width, height))
    out_vid.write(img)
out_vid.release()
print(f"Saved to {out_path}")
