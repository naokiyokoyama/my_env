import argparse
import os.path as osp

import cv2
import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("video_path")
parser.add_argument("speedup_by", type=float)
parser.add_argument("--out_path")
args = parser.parse_args()

if args.out_path is None:
    basename = osp.basename(args.video_path)
    new_basename = f"{args.speedup_by}x_{basename}"
    args.out_path = args.video_path.replace(basename, new_basename)

in_vid = cv2.VideoCapture(args.video_path)
fps = in_vid.get(cv2.CAP_PROP_FPS)
total_frames = in_vid.get(cv2.CAP_PROP_FRAME_COUNT)
four_cc = cv2.VideoWriter_fourcc(*"MP4V")

ret, frame = in_vid.read()
height, width = frame.shape[:2]

out_vid = cv2.VideoWriter(args.out_path, four_cc, fps, (width, height))

print(f"Saving sped-up video to {args.out_path}...")
save_checkpoint = 0
count = 0
save_interval = args.speedup_by / total_frames
for frame_idx in tqdm.trange(1, int(total_frames)):
    if frame_idx / total_frames >= save_checkpoint:
        save_checkpoint += save_interval
        out_vid.write(frame)
        count += 1
    ret, frame = in_vid.read()
out_vid.release()
print("Original frame count:", total_frames)
print("New frame count:", count)
print(f"{total_frames} / {count} = {total_frames / count}")
