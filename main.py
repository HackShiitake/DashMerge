import os
import datetime
import subprocess

TARGET_DIR = "./DCIM"
VIDEO_EXT = ".avi"
TEMP_DIR = "./temp"

os.makedirs(TEMP_DIR, exist_ok=True)

video_files = [
    f for f in os.listdir(TARGET_DIR)
    if f.lower().endswith(VIDEO_EXT)
]

video_groups = {}
for file in video_files:
    path = os.path.join(TARGET_DIR, file)
    created_timestamp = os.path.getmtime(path)
    created_date = datetime.datetime.fromtimestamp(created_timestamp).strftime("%Y%m%d")
    video_groups.setdefault(created_date, []).append((created_timestamp, file))

for date, files_with_time in video_groups.items():
    print(f"\n📅 Processing date: {date}")
    sorted_files = sorted(files_with_time, key=lambda x: x[0])

    temp_files = []
    for i, (_, file) in enumerate(sorted_files):
        input_path = os.path.join(TARGET_DIR, file)
        temp_path = os.path.join(TEMP_DIR, f"{date}_part{i:03}.mp4")
        print(f"🎞️ Converting {file} → {temp_path}")

        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-movflags", "+faststart",
            temp_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        temp_files.append(temp_path)

    list_path = os.path.join(TEMP_DIR, f"{date}_list.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for temp_file in temp_files:
            f.write(f"file '{os.path.abspath(temp_file)}'\n")

    output_path = os.path.join(TARGET_DIR, f"{date}_merged.mp4")
    print(f"🔗 Merging {len(temp_files)} clips → {output_path}")

    merge_cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
        "-c", "copy", output_path
    ]
    subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for temp_file in temp_files:
        os.remove(temp_file)
    os.remove(list_path)

print("\n✅ Complete!")
