# DashMerge

Convert AVI dashcam videos to MP4, sort them by recording date, and merge them into daily videos.

## Features
- Converts `.avi` files to `.mp4` using FFmpeg
- Groups and merges videos by recording date
- Outputs one MP4 file per day
- Cleans up temporary files after processing

## Requirements
- Python 3.x
- FFmpeg (must be in your PATH)

## Usage
Place your AVI files in the `./DCIM` directory, then run:

```bash
python main.py
