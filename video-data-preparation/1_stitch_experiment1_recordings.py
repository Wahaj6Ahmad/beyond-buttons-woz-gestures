# It’s a batch “stitch my raw recordings into one video per camera per participant” script.

# Briefly, it:

# Looks inside User_Recordings/ for participant folders like P001, P002, etc.

# For each participant, it creates (in User_Recordings/Experiment_1/):

# Pxxx_E1_front.mp4 (from front camera files)

# Pxxx_E1_top.mp4 (from GoPro/top files)

# Pxxx_E1_screen.mp4 (from screen recording)

# How it builds them:

# Front: finds .mts files in Pxxx/front/, converts them to mp4 if needed, then concatenates them into one ..._front.mp4.

# Top/GoPro: finds .mp4 chunks in Pxxx/gopro/, concatenates them into one ..._top.mp4, and deletes GoPro sidecar files (.lrv, .thm).

# Screen: finds a single .mp4 in Pxxx/screen/ and just copies it into ..._screen.mp4 using ffmpeg stream copy.

# It also skips a participant if all three output videos already exist.

import os
import subprocess

BASE_DIR = "User_Recordings"
OUTPUT_DIR = os.path.join(BASE_DIR, "Experiment_1")

def run_ffmpeg(cmd):
    """Run ffmpeg command safely."""
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def convert_and_concat(input_files, output_file):
    """
    Convert input files to mp4 (if needed) and concatenate them.
    """
    temp_dir = os.path.dirname(output_file)
    txt_list = os.path.join(temp_dir, "concat_list.txt")

    converted_files = []
    for i, f in enumerate(sorted(input_files)):
        base, ext = os.path.splitext(f)
        out_file = f"{base}_converted.mp4" if ext.lower() != ".mp4" else f
        if ext.lower() != ".mp4":
            run_ffmpeg(["ffmpeg", "-y", "-i", f, "-c:v", "copy", "-c:a", "aac", out_file])
        converted_files.append(out_file)

    # Write concat list
    with open(txt_list, "w", encoding="utf-8") as f:
        for cf in converted_files:
            f.write(f"file '{os.path.abspath(cf)}'\n")

    # Concatenate
    run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", txt_list, "-c", "copy", output_file])

    # Clean temp converted files if they were created
    for cf in converted_files:
        if "_converted.mp4" in cf:
            os.remove(cf)
    os.remove(txt_list)

def process_participant(p_dir):
    pid = os.path.basename(p_dir)

    # Output filenames
    out_front = os.path.join(OUTPUT_DIR, f"{pid}_E1_front.mp4")
    out_top = os.path.join(OUTPUT_DIR, f"{pid}_E1_top.mp4")
    out_screen = os.path.join(OUTPUT_DIR, f"{pid}_E1_screen.mp4")

    # ✅ Skip participant if all outputs already exist
    if all(os.path.exists(f) for f in [out_front, out_top, out_screen]):
        print(f"⏩ Skipping {pid}, outputs already exist.")
        return

    # FRONT (MTS -> MP4 -> stitch)
    front_dir = os.path.join(p_dir, "front")
    if not os.path.exists(out_front) and os.path.exists(front_dir):
        mts_files = [os.path.join(front_dir, f) for f in os.listdir(front_dir) if f.lower().endswith(".mts")]
        if mts_files:
            convert_and_concat(mts_files, out_front)

    # GOPRO (MP4 -> stitch, delete .lrv and .thm)
    gopro_dir = os.path.join(p_dir, "gopro")
    if not os.path.exists(out_top) and os.path.exists(gopro_dir):
        mp4_files = [os.path.join(gopro_dir, f) for f in os.listdir(gopro_dir) if f.lower().endswith(".mp4")]
        if mp4_files:
            convert_and_concat(mp4_files, out_top)
        # Remove .lrv and .thm
        for f in os.listdir(gopro_dir):
            if f.lower().endswith((".lrv", ".thm")):
                os.remove(os.path.join(gopro_dir, f))
                print(f"Deleted {f}")

    # SCREEN (copy single mp4)
    screen_dir = os.path.join(p_dir, "screen")
    if not os.path.exists(out_screen) and os.path.exists(screen_dir):
        mp4_files = [os.path.join(screen_dir, f) for f in os.listdir(screen_dir) if f.lower().endswith(".mp4")]
        if mp4_files:
            # Assume only one screen recording
            run_ffmpeg(["ffmpeg", "-y", "-i", mp4_files[0], "-c", "copy", out_screen])

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for entry in os.listdir(BASE_DIR):
        p_dir = os.path.join(BASE_DIR, entry)
        if os.path.isdir(p_dir) and entry.startswith("P"):
            print(f"\nProcessing {entry}...")
            process_participant(p_dir)

if __name__ == "__main__":
    main()
