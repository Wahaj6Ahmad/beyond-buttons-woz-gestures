# Video Preprocessing Pipeline (WoZ Gesture Study)

This folder contains a small, numbered pipeline of scripts to turn raw recordings into **clean, synchronized videos** that are easy to **watch, review, and annotate** (e.g., in ELAN).

The typical flow is:

1) stitch raw camera chunks into one file per camera  
2) compress / standardize frame rate where needed  
3) sync front + top + screen using clap times into a single stacked video  

---

## What you get at the end

For each participant (e.g., `P001`), you end up with a single file like:

- `synced_outputs/P001_synced.mp4`

This final synced video shows:

- **Front view + Top view + Screen view** side-by-side (horizontally stacked)  
- aligned using the **clap** moment you logged in `clap_times.xlsx`

These synced videos are ideal for annotation because:
- the views are aligned in time
- frame rate is constant (50 fps)
- you can scrub and annotate confidently without drift

---

## Requirements

- Python 3.9+ recommended
- `ffmpeg` and `ffprobe` available in your PATH  
  - Verify: `ffmpeg -version` and `ffprobe -version`
- Python packages:
  - `pandas` (needed for the sync script)

Install pandas if needed:
```bash
pip install pandas
