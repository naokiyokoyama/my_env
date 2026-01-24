#!/usr/bin/env python3
"""
Compress a video file using H.264/AAC encoding.

Usage:
    python compress_video.py input.mov [output.mov]
    
If no output path is specified, creates input_compressed.mov
"""

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_CRF = 28
DEFAULT_PRESET = 'medium'


def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def compress_video(input_path: Path, output_path: Path, crf: int, preset: str) -> bool:
    """Compress a video file using ffmpeg with H.264 codec."""
    
    suffix = output_path.suffix.lower()
    format_args = ['-f', 'mov'] if suffix == '.mov' else ['-f', 'mp4']
    
    cmd = [
        'ffmpeg', '-y', '-i', str(input_path),
        '-c:v', 'libx264',
        '-preset', preset,
        '-crf', str(crf),
        '-profile:v', 'high',
        '-level', '4.1',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-pix_fmt', 'yuv420p',
        *format_args,
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description='Compress a video file')
    parser.add_argument('input', help='Input video file')
    parser.add_argument('output', nargs='?', help='Output video file (optional)')
    parser.add_argument('--crf', type=int, default=DEFAULT_CRF,
                        help=f'Quality (0-51, lower=better, default={DEFAULT_CRF})')
    parser.add_argument('--preset', default=DEFAULT_PRESET,
                        choices=['ultrafast', 'superfast', 'veryfast', 'faster', 
                                'fast', 'medium', 'slow', 'slower', 'veryslow'],
                        help=f'Speed/quality tradeoff (default={DEFAULT_PRESET})')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    # Determine output path (preserve original extension)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_stem(input_path.stem + '_compressed')
    
    # Check for ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: ffmpeg not found. Install with: brew install ffmpeg")
        sys.exit(1)
    
    original_size = input_path.stat().st_size
    print(f"Input:    {input_path} ({format_size(original_size)})")
    print(f"Output:   {output_path}")
    print(f"Settings: CRF={args.crf}, preset={args.preset}")
    print()
    print("Compressing...")
    
    if compress_video(input_path, output_path, args.crf, args.preset):
        new_size = output_path.stat().st_size
        saved = original_size - new_size
        print(f"Done! {format_size(original_size)} → {format_size(new_size)}", end='')
        if saved > 0:
            print(f" (saved {format_size(saved)}, {100*saved/original_size:.1f}%)")
        else:
            print(f" (file grew by {format_size(-saved)})")
    else:
        print("Error: Compression failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
