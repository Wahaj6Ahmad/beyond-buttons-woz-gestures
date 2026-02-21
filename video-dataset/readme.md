Gesture Mini-Clip Dataset (Wizard-of-Oz Fighting Game Study)
==============================================================

1. OVERVIEW
-----------

This dataset contains segmented video clips of hand gestures collected during a
Wizard-of-Oz user study investigating gesture-based control for fighting games
(using Tekken 8 as a testbed).

Each clip contains a single annotated gesture event, centered within the video,
with temporal buffer before and after the gesture.

The dataset is fully anonymised. All audio has been removed.


2. STUDY CONTEXT (BRIEF)
------------------------

The data was collected as part of an MSc thesis in Interaction Technology at
the University of Twente.

Participants were asked to perform hand gestures corresponding to fighting-game
actions (e.g., forward, backward, punch, kick, multi-hit moves). The system
operated in a Wizard-of-Oz configuration, where gestures were interpreted by a
human operator rather than an automatic recogniser.

The study included:
- Controlled prompt-based gesture production
- Increasing speed conditions
- Multimodal recording (front view, top view, screen recording, audio)

Only the hand-gesture video data is included in this dataset.


3. DATASET STRUCTURE
--------------------

Each participant folder contains two camera views:

P001/
    front/
    top/
P002/
    ...
P010/

Front View:
- Captures the participant from the front.
- Shows hand configuration, arm movement, and gross body posture.
- Suitable for handshape analysis and gesture articulation modelling.

Top View:
- Overhead camera angle.
- Emphasizes spatial direction and movement trajectories.
- Suitable for motion path and directional intent analysis.


4. CLIP CONSTRUCTION
--------------------

Each mini clip:
- Corresponds to one annotated gesture event.
- Is centered on the gesture.
- Includes approximately 2.5 seconds before and 2.5 seconds after.

This buffer ensures:
- Temporal context
- Capture of preparation and retraction phases
- Robustness to minor annotation offsets

Important:
Because of this buffer, a clip may contain:
- Partial previous gestures
- Partial subsequent gestures
- Occasionally complete neighbouring gestures

The primary gesture of interest is always centered in the clip.


5. AUDIO AND ANONYMISATION
--------------------------

- All audio tracks have been removed.
- No speech data is included.
- No personally identifying information is present.
- Participants are referenced only by anonymised IDs (P001–P010).
- Screen recordings are not included.
- No personal metadata is provided.

This dataset is suitable for public academic use.


6. DATA PROCESSING PIPELINE (HIGH LEVEL)
----------------------------------------

1. Participants were recorded using synchronized multi-camera capture.
2. Gesture events were annotated in ELAN.
3. Annotation timestamps were exported.
4. Each gesture event was extracted from synchronized video.
5. A ±2.5 second buffer was added.
6. Clips were saved as individual MP4 files.
7. Audio streams were removed using ffmpeg.
8. Files were organized per participant and camera view.

The exported clips preserve the original video stream where possible.


7. POTENTIAL USES
-----------------

This dataset may be used for:

- Gesture recognition research
- Vision-based hand movement modelling
- Gesture segmentation research
- Motion trajectory analysis
- Embodied interaction studies
- Human-computer interaction research
- Fighting game input design research
- Robustness evaluation under speed constraints

Because gestures were elicited in a controlled speed-ramp condition, the
dataset contains:

- Full gestures
- Compressed gestures under time pressure
- Natural simplifications
- Occasional breakdowns


8. LIMITATIONS
--------------

- Dataset size: 10 participants
- Controlled prompt-following context (not free gameplay)
- Buffers may include adjacent gestures
- Lighting and recording conditions reflect lab setup
- No depth data
- No motion capture ground truth


9. CITATION
-----------

If you use this dataset, please cite:

Wahaj Ahmad.
Exploring the Design Potential of Wizard-of-Oz Elicited Hand Gestures for
Fighting Game Control.
MSc Thesis, University of Twente, 2026.

(Include DOI once assigned by Zenodo.)


10. CONTACT
-----------

For questions regarding the dataset, please contact:

[Your academic email]
