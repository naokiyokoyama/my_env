import argparse
import os
import re
import sys
from urllib.parse import urljoin, urlparse

import cv2
import requests


def download_file(url, filepath):
    """Download a file from URL to filepath"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def is_landscape(image_path):
    """Check if image is landscape (wider than tall)"""
    try:
        # cv2.imread returns None if file cannot be read
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not read image: {image_path}")
            return False

        # img.shape returns (height, width, channels) for color images
        # or (height, width) for grayscale images
        height, width = img.shape[:2]
        return width >= height
    except Exception as e:
        print(f"Error checking dimensions of {image_path}: {e}")
        return False


def convert_github_url_to_raw(url):
    """Convert GitHub blob URL to raw URL"""
    if "github.com" in url and "/blob/" in url:
        # Convert github.com/user/repo/blob/branch/path to raw.githubusercontent.com/user/repo/branch/path
        url = url.replace("github.com/", "raw.githubusercontent.com/")
        url = url.replace("/blob/", "/")
    return url


def find_jpg_urls_regex(html_content, base_url):
    """Find all JPG URLs in HTML content using regex"""
    image_urls = set()

    # Pattern for img src attributes: <img ... src="image.jpg" ...>
    img_src_pattern = re.compile(
        r'<img[^>]+src=["\']([^"\']*\.jpe?g)["\']', re.IGNORECASE
    )
    for match in img_src_pattern.finditer(html_content):
        image_urls.add(match.group(1))

    # Pattern for a href attributes: <a ... href="image.jpg" ...>
    a_href_pattern = re.compile(
        r'<a[^>]+href=["\']([^"\']*\.jpe?g)["\']', re.IGNORECASE
    )
    for match in a_href_pattern.finditer(html_content):
        image_urls.add(match.group(1))

    # Pattern for data-src attributes (lazy loading): data-src="image.jpg"
    data_src_pattern = re.compile(r'data-src=["\']([^"\']*\.jpe?g)["\']', re.IGNORECASE)
    for match in data_src_pattern.finditer(html_content):
        image_urls.add(match.group(1))

    # Pattern for data-fancybox attributes (fancybox galleries): data-fancybox="gallery" href="image.jpg"
    fancybox_pattern = re.compile(
        r'data-fancybox=["\'][^"\']*["\'][^>]+href=["\']([^"\']*\.jpe?g)["\']',
        re.IGNORECASE,
    )
    for match in fancybox_pattern.finditer(html_content):
        image_urls.add(match.group(1))

    # Pattern for any JPG URLs in quotes (catches JavaScript arrays, JSON, etc.)
    # More restrictive to avoid capturing malformed URLs
    general_jpg_pattern = re.compile(r'["\']([^"\']*\.jpe?g)["\']', re.IGNORECASE)
    for match in general_jpg_pattern.finditer(html_content):
        url = match.group(1)
        # Skip data URLs, very short URLs, and URLs that look malformed
        if (
            not url.startswith("data:")
            and len(url) > 10
            and not url.startswith('"')
            and not url.endswith('"')
            and ("/" in url or url.startswith("http"))
        ):
            image_urls.add(url)

    # Pattern for URLs without quotes (less common but possible)
    unquoted_jpg_pattern = re.compile(
        r"(?:src|href|data-src)=([^\s>]*\.jpe?g)", re.IGNORECASE
    )
    for match in unquoted_jpg_pattern.finditer(html_content):
        image_urls.add(match.group(1))

    # Convert relative URLs to absolute URLs and fix GitHub URLs
    absolute_urls = []
    for url in image_urls:
        # Clean up the URL (remove any leading/trailing whitespace and quotes)
        url = url.strip().strip('"').strip("'")
        if not url:
            continue

        # Convert GitHub blob URLs to raw URLs
        url = convert_github_url_to_raw(url)

        if url.startswith("http"):
            absolute_urls.append(url)
        else:
            # Handle relative URLs
            if url.startswith("//"):
                # Protocol-relative URL
                absolute_urls.append("https:" + url)
            else:
                absolute_urls.append(urljoin(base_url, url))

    return list(set(absolute_urls))  # Remove duplicates


def main():
    parser = argparse.ArgumentParser(
        description="Download JPG images from Naoki Yokoyama's photos page"
    )
    parser.add_argument("folder", help="Folder to save images in")
    parser.add_argument(
        "--html-url",
        default="https://raw.githubusercontent.com/naokiyokoyama/naokiyokoyama.github.io/refs/heads/master/photos.html",
        help="URL of the HTML file to parse (default: Naoki's photos page)",
    )
    parser.add_argument(
        "--base-url",
        default="https://naokiyokoyama.github.io/",
        help="Base URL for resolving relative image paths",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show all found URLs before filtering",
    )
    args = parser.parse_args()

    # Create output folder if it doesn't exist
    os.makedirs(args.folder, exist_ok=True)

    print(f"Downloading HTML from {args.html_url}")

    try:
        response = requests.get(args.html_url, timeout=30)
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        print(f"Error downloading HTML: {e}")
        sys.exit(1)

    # Find all JPG URLs
    image_urls = find_jpg_urls_regex(html_content, args.base_url)

    if args.verbose:
        print(f"\nAll found JPG URLs ({len(image_urls)}):")
        for url in sorted(image_urls):
            print(f"  {url}")
        print()

    # Filter out thumbnails (containing 'thumb' in the URL)
    filtered_urls = [url for url in image_urls if "thumb" not in url.lower()]

    if args.verbose and len(filtered_urls) != len(image_urls):
        print(f"Filtered out {len(image_urls) - len(filtered_urls)} thumbnail URLs")
        print("Remaining URLs after filtering:")
        for url in filtered_urls[:10]:  # Show first 10
            print(f"  {url}")
        if len(filtered_urls) > 10:
            print(f"  ... and {len(filtered_urls) - 10} more")
        print()

    if not filtered_urls:
        print("No JPG images found in the HTML (excluding thumbnails)")
        print("This might be because:")
        print("1. Images are loaded dynamically with JavaScript")
        print("2. Images are in a different format or location")
        print("3. All images contain 'thumb' in their URLs")
        print(f"\nTotal URLs found before filtering: {len(image_urls)}")
        if image_urls:
            print("Found URLs:")
            for url in image_urls[:10]:  # Show first 10
                print(f"  {url}")
            if len(image_urls) > 10:
                print(f"  ... and {len(image_urls) - 10} more")
        print("\nHTML content preview (first 1000 chars):")
        print(html_content[:1000] + "..." if len(html_content) > 1000 else html_content)
        return

    print(f"Found {len(filtered_urls)} JPG images to download (excluding thumbnails)")

    # Download images
    downloaded_files = []

    for i, url in enumerate(filtered_urls, 1):
        # Get filename from URL
        filename = os.path.basename(urlparse(url).path)
        if not filename or not filename.lower().endswith((".jpg", ".jpeg")):
            filename = f"image_{i}.jpg"

        # Avoid filename conflicts
        filepath = os.path.join(args.folder, filename)
        counter = 1
        while os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            filepath = os.path.join(args.folder, f"{name}_{counter}{ext}")
            counter += 1

        print(f"Downloading {url} -> {os.path.basename(filepath)}")
        if download_file(url, filepath):
            downloaded_files.append(filepath)

    if not downloaded_files:
        print("No images were successfully downloaded")
        return

    # Check dimensions and delete portrait images
    print(f"\nChecking dimensions of {len(downloaded_files)} downloaded images...")
    kept_count = 0
    deleted_count = 0

    for filepath in downloaded_files:
        if is_landscape(filepath):
            print(f"✓ Keeping landscape image: {os.path.basename(filepath)}")
            kept_count += 1
        else:
            print(f"✗ Deleting portrait image: {os.path.basename(filepath)}")
            try:
                os.remove(filepath)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")

    print(
        f"\n🎉 Done! Kept {kept_count} landscape images, deleted {deleted_count} portrait images."
    )
    print(f"Images saved in: {os.path.abspath(args.folder)}")


if __name__ == "__main__":
    main()
