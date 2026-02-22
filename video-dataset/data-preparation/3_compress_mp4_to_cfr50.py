# This script is a simple “compress and force 50fps CFR” batch converter for MP4 files in the current folder.

# Briefly, it:

# Looks in the current directory (INPUT_DIR = ".") for every .mp4.

# Creates an output folder called compressed/.

# For each video, runs ffmpeg to:

# force constant frame rate 50 fps (-vf fps=50 + -vsync cfr)

# re-encode video to H.264 (libx264) with CRF 30 and ultrafast preset (fast, but lower efficiency/quality)

# re-encode audio to AAC 128 kbps

# set pixel format to yuv420p (compatibility)

# Saves the converted file with the same filename inside compressed/.

import os
import subprocess

# === CONFIG ===
INPUT_DIR = "."                     # current folder
OUTPUT_DIR = "compressed"           # new folder
TARGET_FPS = 50                     # constant frame rate

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through all .mp4 files
for file in os.listdir(INPUT_DIR):
    if file.lower().endswith(".mp4"):
        input_path = os.path.join(INPUT_DIR, file)
        output_path = os.path.join(OUTPUT_DIR, file)

        # ffmpeg command
        cmd = [
            "ffmpeg", "-i", input_path,
            "-vf", f"fps={TARGET_FPS}",
            "-vsync", "cfr",
            "-c:v", "libx264", "-crf", "30", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            output_path
        ]

        print(f"Processing {file} → {output_path}")
        subprocess.run(cmd, check=True)

print("✅ All videos converted to CFR 50fps and compressed!")
