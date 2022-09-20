import argparse

from moviepy.editor import VideoFileClip, vfx


def main(video, speedup, out_path):
    clip = VideoFileClip(video)
    clip = clip.fx(vfx.speedx, speedup)
    out_path = f"{speedup}_{out_path}"
    clip.write_videofile(out_path, fps=30)
    print(f"Saved output video to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("speedup", type=float, help="Speed up factor")
    parser.add_argument("-o", "--out-path", default="out.mp4")
    args = parser.parse_args()
    main(args.video, args.speedup, args.out_path)
