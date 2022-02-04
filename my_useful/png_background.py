"""
Convert 4 channel png to a 3 channel png by coloring transparent pixels
with alpha channel weighting
"""

import argparse
import os.path as osp

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("png_path", help="path to png")
    parser.add_argument(
        "-p", "--pixel_value", default="255,255,255", help="desired background color"
    )
    parser.add_argument("-o", "--out_path", help="default: png_path prefixed with 'b_'")
    args = parser.parse_args()
    assert args.png_path.lower().endswith(".png"), "Not a png."

    if args.out_path is None:
        basename = osp.basename(args.png_path)
        args.out_path = args.png_path.replace(basename, "b_" + basename)

    img = cv2.imread(args.png_path, cv2.IMREAD_UNCHANGED)
    background = np.ones([*img.shape[:2], 3], dtype=np.uint8)
    pixel_value = tuple([int(i) for i in args.pixel_value.split(",")])
    background[:, :] = pixel_value
    img = overlay_transparent(background, img, 0, 0)

    cv2.imwrite(args.out_path, img)
    print(f"Saved to {args.out_path}!")


# https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
def overlay_transparent(background, overlay, x, y):

    background_height, background_width = background.shape[:2]
    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[:2]
    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype)
                * 255,
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y : y + h, x : x + w] = (1.0 - mask) * background[
        y : y + h, x : x + w
    ] + mask * overlay_image

    return background


if __name__ == "__main__":
    main()
