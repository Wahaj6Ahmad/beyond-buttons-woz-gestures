It’s a batch “stitch my raw recordings into one video per camera per participant” script.

Briefly, it:

Looks inside User_Recordings/ for participant folders like P001, P002, etc.

For each participant, it creates (in User_Recordings/Experiment_1/):

Pxxx_E1_front.mp4 (from front camera files)

Pxxx_E1_top.mp4 (from GoPro/top files)

Pxxx_E1_screen.mp4 (from screen recording)

How it builds them:

Front: finds .mts files in Pxxx/front/, converts them to mp4 if needed, then concatenates them into one ..._front.mp4.

Top/GoPro: finds .mp4 chunks in Pxxx/gopro/, concatenates them into one ..._top.mp4, and deletes GoPro sidecar files (.lrv, .thm).

Screen: finds a single .mp4 in Pxxx/screen/ and just copies it into ..._screen.mp4 using ffmpeg stream copy.

It also skips a participant if all three output videos already exist.
