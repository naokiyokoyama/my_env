import argparse
import os.path as osp

import cv2
import numpy as np
import tqdm

parser = argparse.ArgumentParser(
    description=(
        "Stack videos vertically or horizontally. Example usage:\n"
        "python stack_videos.py path/to/vid1 path/to/vid2 ... -t"
    )
)
parser.add_argument("video_files", nargs="+")
parser.add_argument(
    "-t", "--truncate", help="duration is equal to shortest video", action="store_true"
)
parser.add_argument(
    "-u", "--upscale", help="all videos are upscaled to size of largest video"
)
parser.add_argument(
    "-v",
    "--vertical",
    help="stack videos vertically, not horizontally",
    action="store_true",
)
args = parser.parse_args()

videos = []
for v in args.video_files:
    assert osp.isfile(v), f"{v} does not exist!"
    videos.append(cv2.VideoCapture(v))

frame_counts = sorted(v.get(cv2.CAP_PROP_FRAME_COUNT) for v in videos)
frame_count_idx = 0 if args.truncate else -1
output_frame_count = frame_counts[frame_count_idx]

fps = videos[0].get(cv2.CAP_PROP_FPS)
four_cc = cv2.VideoWriter_fourcc(*"MP4V")
output_path = "stacked_output.mp4"
out_vid = None
dim_idx = 1 if args.vertical else 0
sort_idx = 0 if args.upscale else -1
prev_frames = [None] * len(videos)
for _ in tqdm.trange(int(output_frame_count)):
    new_frames = [v.read() for v in videos]
    frames = [n[1] if n[0] else p for n, p in zip(new_frames, prev_frames)]

    largest_dim = sorted([f.shape[dim_idx] for f in frames])[sort_idx]
    new_dim = [0, 0]
    new_dim[dim_idx] = largest_dim
    resized_frames = []
    other_dim_idx = (dim_idx + 1) % 2
    for f in frames:
        new_dim[other_dim_idx] = int(
            f.shape[other_dim_idx] * largest_dim / f.shape[dim_idx]
        )
        resized_frames.append(cv2.resize(f, new_dim[::-1]))
    if args.vertical:
        frame = np.vstack(resized_frames)
    else:
        frame = np.hstack(resized_frames)

    if out_vid is None:
        height, width = frame.shape[:2]
        out_vid = cv2.VideoWriter(output_path, four_cc, fps, (width, height))

    out_vid.write(frame)
    prev_frames = frames

out_vid.release()
print(f"Saved video to {osp.abspath(output_path)}")
