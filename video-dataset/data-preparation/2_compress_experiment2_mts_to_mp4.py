# This one is a batch converter/compressor for Experiment 2.

# Briefly, it:

# Scans Experiment_2/ for participant folders (skips the compressed/ folder).

# Finds all .MTS videos inside each participant folder.

# Converts each .MTS to a compressed .mp4 and saves it into:

# Experiment_2/compressed/<participant>/<same_name>.mp4

# Conversion settings:

# Re-encodes video to H.264 (libx264) with:

# preset = ultrafast (fast encoding, larger files / lower efficiency)

# crf = 30 (more compression, lower quality than e.g. 23)

# Forces 50 fps constant frame rate (fps=50 + -vsync cfr)

# yuv420p pixel format (widest compatibility)

# Encodes audio to AAC 128 kbps

# Convenience features:

# Skips files that already have an output .mp4

# Prints progress + per-file time + rough ETA

import os
import subprocess
import time

# === CONFIG ===
BASE_DIR = "Experiment_2"
OUTPUT_ROOT = os.path.join(BASE_DIR, "compressed")
TARGET_FPS = 50
CRF = 30
PRESET = "ultrafast"

# Create compressed root if not exists
os.makedirs(OUTPUT_ROOT, exist_ok=True)

# Collect all .MTS videos first
video_list = []
for participant in os.listdir(BASE_DIR):
    participant_path = os.path.join(BASE_DIR, participant)
    if not os.path.isdir(participant_path) or participant == "compressed":
        continue

    output_folder = os.path.join(OUTPUT_ROOT, participant)
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(participant_path):
        if file.lower().endswith(".mts"):
            input_path = os.path.join(participant_path, file)
            base_name = os.path.splitext(file)[0]
            output_path = os.path.join(output_folder, f"{base_name}.mp4")
            video_list.append((input_path, output_path))

total_videos = len(video_list)
if total_videos == 0:
    print("⚠️  No MTS videos found.")
    exit()

print(f"🎬 Found {total_videos} MTS videos to process.\n")

# Process videos
start_time = time.time()
completed = 0
total_processing_time = 0

for idx, (input_path, output_path) in enumerate(video_list, 1):
    if os.path.exists(output_path):
        print(f"⏭️  Skipping ({idx}/{total_videos}): {os.path.basename(output_path)} (already converted)")
        continue

    print(f"\n▶️  Converting ({idx}/{total_videos}): {os.path.basename(input_path)}")

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", PRESET,
        "-crf", str(CRF),
        "-vf", f"fps={TARGET_FPS}",
        "-vsync", "cfr",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        output_path,
        "-hide_banner", "-loglevel", "error"
    ]

    t0 = time.time()
    subprocess.run(cmd, check=True)
    elapsed = time.time() - t0

    completed += 1
    total_processing_time += elapsed
    avg_time = total_processing_time / completed
    remaining = avg_time * (total_videos - completed)

    print(f"✅ Done ({completed}/{total_videos}) | ⏱️ {elapsed/60:.1f} min | ETA ≈ {remaining/60:.1f} min")

total_time = time.time() - start_time
print(f"\n🎉 All conversions complete! Total time: {total_time/60:.1f} min")
print(f"Converted files saved in: {OUTPUT_ROOT}")
