# This script **synchronizes (“aligns”) three video recordings per participant using clap times**, then outputs a single **side-by-side stacked** video.

# Briefly, it does this:

# * Reads `clap_times.xlsx` to get, for each participant:

#   * `t_screen`, `t_front`, `t_top` (when the clap happens in each recording)
# * Uses the **screen clap time as the reference**.
# * Computes offsets:

#   * `offset_front = t_front - t_screen`
#   * `offset_top = t_top - t_screen`
#   * screen offset is set to 0

# Then for each participant it runs ffmpeg to:

# * If a camera’s clap happens **later** than the screen:

#   * it **trims** the start of that stream (so it “catches up”)
# * If a camera’s clap happens **earlier** than the screen:

#   * it **pads/delays** the start (adds blank time at the beginning)
#   * for front audio it uses `adelay`; for video it uses `tpad`

# After alignment it:

# * Scales all streams to the **screen recording’s resolution**
# * Forces **50 fps**
# * Stacks the three videos horizontally:

#   * `[front][top][screen]hstack=inputs=3`
# * Keeps **front audio** as the output audio track
# * Writes the result to `synced_outputs/Pxxx_synced.mp4`

# Extra behavior:

# * If you type a single participant ID (not `all`), it runs in **test mode** and only exports the first **120 seconds** (`-t 120`) to save time while checking alignment.


import os
import subprocess
import pandas as pd

# === CONFIG ===
EXCEL_FILE = "clap_times.xlsx"   # your excel file
VIDEO_DIR = "."                  # folder with videos
OUTPUT_DIR = "synced_outputs"
FPS = 50                         # target fps
TEST_DURATION = 120              # 2 minutes (seconds)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_time(ts: str) -> float:
    """Parse timestamp in mm:ss:ff format into seconds (float)."""
    if pd.isna(ts):
        return 0.0
    ts = str(ts).strip()
    parts = ts.split(":")
    if len(parts) == 3:
        mm, ss, ff = parts
        return int(mm) * 60 + float(f"{ss}.{ff}")
    elif len(parts) == 2:
        mm, ss = parts
        return int(mm) * 60 + float(ss)
    else:
        return float(ts)

def get_resolution(video_path):
    """Get width and height of a video using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0:s=x",
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    w, h = result.stdout.strip().split("x")
    return int(w), int(h)

def build_filter(offset_front, offset_top, offset_screen, width, height):
    """Build FFmpeg filter string with correct trim/delay logic."""

    filters = []

    # --- FRONT video & audio ---
    if offset_front > 0:  # clap is later → trim beginning
        filters.append(f"[0:v]fps={FPS},scale={width}:{height},trim=start={offset_front},setpts=PTS-STARTPTS[front]")
        filters.append(f"[0:a]atrim=start={offset_front},asetpts=PTS-STARTPTS[aud]")
    else:  # clap is earlier → delay
        delay_ms = int(abs(offset_front) * 1000)
        filters.append(f"[0:v]fps={FPS},scale={width}:{height},tpad=start_duration={-offset_front}[front]")
        filters.append(f"[0:a]adelay={delay_ms}|{delay_ms}[aud]")

    # --- TOP video ---
    if offset_top > 0:
        filters.append(f"[1:v]fps={FPS},scale={width}:{height},trim=start={offset_top},setpts=PTS-STARTPTS[top]")
    else:
        filters.append(f"[1:v]fps={FPS},scale={width}:{height},tpad=start_duration={-offset_top}[top]")

    # --- SCREEN video ---
    if offset_screen > 0:
        filters.append(f"[2:v]fps={FPS},scale={width}:{height},trim=start={offset_screen},setpts=PTS-STARTPTS[screen]")
    else:
        filters.append(f"[2:v]fps={FPS},scale={width}:{height},tpad=start_duration={-offset_screen}[screen]")

    # --- Stack video streams ---
    filters.append("[front][top][screen]hstack=inputs=3[v]")

    return "; ".join(filters)

# === MAIN ===
df = pd.read_excel(EXCEL_FILE)
choice = input("Enter participant ID (e.g., P001) or 'all': ").strip()

if choice.lower() == "all":
    participants = df['Participant_ID'].tolist()
    test_mode = False
else:
    participants = [choice]
    test_mode = True

for participant in participants:
    row = df[df['Participant_ID'] == participant]
    if row.empty:
        print(f"⚠️ Skipping {participant} (not found in Excel)")
        continue

    # Extract clap times
    t_screen = parse_time(row['t_screen'].values[0])
    t_front = parse_time(row['t_front'].values[0])
    t_top = parse_time(row['t_top'].values[0])

    ref = t_screen
    offset_front = t_front - ref
    offset_top = t_top - ref
    offset_screen = 0

    # File paths
    front_file = os.path.join(VIDEO_DIR, f"{participant}_E1_front.mp4")
    top_file = os.path.join(VIDEO_DIR, f"{participant}_E1_top.mp4")
    screen_file = os.path.join(VIDEO_DIR, f"{participant}_E1_screen.mp4")
    output_file = os.path.join(OUTPUT_DIR, f"{participant}_synced.mp4")

    # Detect resolution of screen video
    width, height = get_resolution(screen_file)

    # Build filter
    filter_complex = build_filter(offset_front, offset_top, offset_screen, width, height)

    # ffmpeg command
    cmd = [
        "ffmpeg",
        "-i", front_file,
        "-i", top_file,
        "-i", screen_file,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[aud]",
        "-c:v", "libx264", "-crf", "30", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "128k"
    ]

    # If testing → limit to 2 minutes
    if test_mode:
        cmd += ["-t", str(TEST_DURATION)]

    cmd.append(output_file)

    print(f"🎬 Processing {participant} "
          f"(offsets: front={offset_front:.2f}s, top={offset_top:.2f}s, screen={offset_screen:.2f}s) "
          f"→ {output_file}")

    subprocess.run(cmd, check=True)

print("✅ Done! Videos exported to 'synced_outputs/'")

