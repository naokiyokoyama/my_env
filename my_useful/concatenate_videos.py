import argparse
import os.path as osp

from moviepy.editor import VideoFileClip, concatenate_videoclips


def main(videos, out_path):
    if out_path is None:
        out_path = osp.basename("concatenated_out.mp4")
    clips = [VideoFileClip(v) for v in videos]
    clip = concatenate_videoclips(clips, method="compose")
    clip.write_videofile(out_path, fps=30)
    print(f"Saved output video to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("videos", nargs="+")
    parser.add_argument("-o", "--out-path")
    args = parser.parse_args()
    main(args.videos, args.out_path)
