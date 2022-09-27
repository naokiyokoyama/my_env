import argparse
import os.path as osp

from moviepy.editor import VideoFileClip, concatenate_videoclips


def main(video, out_path, start, end):
    if out_path is None:
        out_path = osp.basename(f"{start}_{end}_{video}")

    # Replace extension with mp4
    out_path = osp.splitext(out_path)[0] + ".mp4"

    clip = VideoFileClip(video)
    trimmed_clip = clip.subclip(start, end)
    trimmed_clip.write_videofile(out_path, fps=30)
    print(f"Saved output video to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("start")
    parser.add_argument("end")
    parser.add_argument("-o", "--out-path")
    args = parser.parse_args()
    main(args.video, args.out_path, args.start, args.end)
