import argparse
import os.path as osp

from moviepy.editor import VideoFileClip, vfx


def main(video, speedup, out_path):
    if out_path is None:
        out_path = osp.basename(video)
    clip = VideoFileClip(video)
    clip = clip.fx(vfx.speedx, speedup)
    out_path = f"{speedup}_{out_path}"
    # Replace extension with mp4
    out_path = osp.splitext(out_path)[0] + ".mp4"
    clip.write_videofile(out_path, fps=30)
    print(f"Saved output video to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("speedup", type=float, help="Speed up factor")
    parser.add_argument("-o", "--out-path")
    args = parser.parse_args()
    main(args.video, args.speedup, args.out_path)
