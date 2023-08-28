import glob
import os
from typing import List

from moviepy.editor import ImageSequenceClip, concatenate_videoclips


def main(images_dir: str):
    """Generates a video from a sequence of images.

    Takes in a directory containing a sequence of images named with timestamps 
    (e.g. from time.time()). Sorts the images by timestamp, converts the timestamps
    to durations in seconds, and generates a video by concatenating clips of each
    image with the corresponding duration.

    Args:
        images_dir: Path to the directory containing the images.

    """
    # Function body...
    img_paths = sorted(
        glob.glob(os.path.join(images_dir, "*.png"))
        + glob.glob(os.path.join(images_dir, "*.jpg")),
        key=lambda x: float(get_basename_no_ext(x)),
    )
    durations = img_paths_to_durations(img_paths)
    generate_video_from_images(img_paths, durations)


def get_basename_no_ext(path: str) -> str:
    """Returns the basename of the given path without the extension.

    Args:
        path: Path to a file.

    Returns:
        The basename of the given path without the extension.
    """
    return os.path.splitext(os.path.basename(path))[0]


def img_paths_to_durations(
    img_paths: List[str], last_duration: float = 1.0
) -> List[float]:
    """
    Generates a list of durations for each image in the given list. The duration that
    each image (except the last frame) is shown is the difference between the basenames
    of the current and next image. The duration of the last image is the given
    last_duration.

    Args:
        img_paths: List of image paths. The basename of each path is a floating point
            number generated using time.time(), plus an image extension.

    Returns:
        List of durations.
    """
    durations = []
    for i in range(len(img_paths) - 1):
        # Get the base names of the current and next image, and remove the extension
        current_basename = os.path.splitext(os.path.basename(img_paths[i]))[0]
        next_basename = os.path.splitext(os.path.basename(img_paths[i + 1]))[0]

        # Convert the base names to floats and calculate the difference
        duration = float(next_basename) - float(current_basename)
        durations.append(duration)

    # Add the last duration
    durations.append(last_duration)

    return durations


def generate_video_from_images(
    img_paths: List[str],
    durations: List[float],
    fps: float = 30.0,
    output_path: str = "output.mp4",
) -> None:
    """
    Generates a video from a list of images, where each image is shown for a specified
    amount of seconds. The two given lists must have the same length.

    Args:
        img_paths: List of image paths.
        durations: List of durations for each image.
        fps: Frames per second.
        output_path: Path to the output video.
    """
    assert len(img_paths) == len(
        durations
    ), "img_paths and durations must have the same length"

    # Create a clip for each image with its corresponding duration
    clips = [
        ImageSequenceClip([img_path], durations=[duration])
        for img_path, duration in zip(img_paths, durations)
    ]

    # Concatenate the clips into a single video
    video = concatenate_videoclips(clips, method="compose")

    # Write the result to a file
    video.write_videofile(output_path, fps=fps)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "images_dir", type=str, help="Path to the directory containing the images."
    )
    args = parser.parse_args()

    main(args.images_dir)
