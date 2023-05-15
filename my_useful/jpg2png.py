import os
import argparse
from PIL import Image

def convert_png_to_jpg(files):
    for file_path in files:
        if file_path.endswith(".png"):
            png_file = file_path
            jpg_file = os.path.splitext(file_path)[0] + ".jpg"

            # Open the PNG file and convert it to JPEG
            image = Image.open(png_file)
            image = image.convert("RGB")

            # Save the image as JPEG
            image.save(jpg_file, "JPEG")
            print(f"Converted {png_file} to {jpg_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG files to JPEG")
    parser.add_argument("files", nargs="+", help="List of PNG files to convert")
    args = parser.parse_args()

    convert_png_to_jpg(args.files)
