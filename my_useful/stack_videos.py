import argparse

import cv2
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from tqdm import tqdm


def stack_videos(video_paths, stack_horizontal, out_path):
    video_data = {k: video_to_dict(k) for k in video_paths}
    new_fps = get_max_fps(video_data.values())
    new_duration = get_max_duration(video_data.values())
    max_num_frames = int(new_fps * new_duration)

    curr_timestep = 0
    frames = []
    with tqdm(total=max_num_frames) as pbar:
        while not all_done(video_data.values()):
            latest_imgs = [v["latest"] for v in video_data.values()]
            frames.append(stack_imgs(latest_imgs, stack_horizontal))
            curr_timestep += 1 / new_fps
            for video_dict in video_data.values():
                step_video_dict(video_dict, curr_timestep)
            pbar.update(1)
    print(f"\nCreating video with {len(frames)} frames..")
    create_video(frames, new_fps, out_path)


def video_to_dict(video_path):
    video = cv2.VideoCapture(video_path)
    ret, frame = video.read()
    video_dict = {"video": video, "ret": ret, "latest": frame}
    assert video_dict["ret"], f"Could not read first frame of video: {video_path}"
    video_dict["fps"] = video.get(cv2.CAP_PROP_FPS)
    video_dict["curr_time"] = 0
    video_dict["duration"] = video.get(cv2.CAP_PROP_FRAME_COUNT) / video_dict["fps"]
    return video_dict


def all_done(video_data_list):
    return all([not v["ret"] for v in video_data_list])


def get_max_fps(video_data_list):
    return max([v["fps"] for v in video_data_list])


def get_max_duration(video_data_list):
    return max([v["duration"] for v in video_data_list])


def step_video_dict(video_dict, curr_timestep):
    """Update the latest image if the given timestep is closer to curr_time + 1/fps"""
    if not video_dict["ret"]:
        return
    timestep = 1 / video_dict["fps"]
    if curr_timestep - video_dict["curr_time"] > timestep:
        video_dict["ret"], frame = video_dict["video"].read()
        if video_dict["ret"]:
            video_dict["curr_time"] += timestep
            video_dict["latest"] = frame


def stack_imgs(imgs, stack_horizontal=False):
    dim_idx = 1 if stack_horizontal else 0
    max_dim = max([i.shape[dim_idx] for i in imgs])
    resized_imgs = []
    for img in imgs:
        curr_dim = img.shape[dim_idx]
        other_dim = img.shape[1 - dim_idx]
        if curr_dim != max_dim:
            new_dim = int(other_dim * (max_dim / curr_dim))
            new_dims = (new_dim, max_dim) if stack_horizontal else (max_dim, new_dim)
            img = cv2.resize(img, new_dims)
        resized_imgs.append(img)
    if stack_horizontal:
        return cv2.hconcat(resized_imgs)
    return cv2.vconcat(resized_imgs)


def create_video(frames, fps, out_path):
    # Convert the list of numpy arrays to a list of RGB images
    frames = [frame[:, :, ::-1] for frame in frames]
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "video_files", nargs="+", help="List of video file paths to be stacked"
    )
    parser.add_argument(
        "-z",
        "--horizontal",
        action="store_true",
        help="Whether to stack horizontally instead of vertically",
    )
    parser.add_argument(
        "-o",
        "--out_path",
        default="stacked.mp4",
        help="Path to output video file (default: stacked.mp4)",
    )
    args = parser.parse_args()
    stacked_frame = stack_videos(args.video_files, args.horizontal, args.out_path)
