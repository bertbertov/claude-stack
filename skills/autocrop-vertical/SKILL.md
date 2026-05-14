---
name: autocrop-vertical
description: Subject-aware reframing of horizontal video to vertical (9:16 / 4:5 / 1:1) using YOLOv8 person detection. Per-scene decision between TRACK (crop tightly on subject) and LETTERBOX (scale + black bars) so people stay centered through cuts and motion. Trigger when user says "reframe to vertical", "16:9 to 9:16", "convert landscape to portrait", "shorts crop", "smart crop for TikTok", "vertical YouTube short from horizontal", "auto-crop interview clip", "reframe podcast video", "make this video vertical", or any equivalent intent. Use as a STAGE inside viral-clipper / book-video / channel-breakdown pipelines whenever the source has more than one person on screen or the subject moves around the frame.
---

# AutoCrop-Vertical — Subject-Aware 16:9 -> 9:16 Reframer

YOLOv8 detects people in each scene's middle frame, then per-scene picks one of two strategies:
- **TRACK** — crop a vertical window centered on the subject(s).
- **LETTERBOX** — scale the full frame down and pad with black bars (used when subjects are too spread out to crop without losing one).

Frame-accurate (no scene-boundary drift), VFR-aware, audio-sync compensated.

## When to use

- Multi-person interview / podcast / two-camera setup → tracking beats center-crop.
- Action scenes, walking-and-talking, B-roll where the subject moves across the frame.
- Cooking / sports / panel discussions where center-crop would chop people in half.
- Inside the **viral-clipper** pipeline: insert this STAGE between clip-cutting and final render. Replace the simple ffmpeg `crop=ih*9/16:ih` step with a call to this script for any clip that has >1 face detected, or whenever the source isn't a static talking head.
- Inside **book-video** / **channel-breakdown**: same — use whenever you cut a horizontal source into vertical Shorts.

## When NOT to use

- Single static talking head dead-center → plain ffmpeg center-crop is faster and identical-looking.
- Already-vertical source → no-op.
- Animation / screen-recording with no people → YOLO has nothing to lock onto; falls back to letterbox anyway, plain center-crop is simpler.
- Sub-3-second clips → scene detection overhead (~50% of runtime) isn't worth it for tiny clips.

## Install location

- **Repo:** `C:\Users\A\Desktop\Autocrop-vertical\`
- **Venv Python:** `C:\Users\A\Desktop\Autocrop-vertical\.venv\Scripts\python.exe` (Python 3.12, CPU torch — torch 2.x has no Python 3.14 wheels yet)
- **Entry script:** `C:\Users\A\Desktop\Autocrop-vertical\main.py`
- **Model:** `yolov8n.pt` (~6 MB, auto-downloads on first run to repo root)
- **Requires:** `ffmpeg` and `ffprobe` on PATH (already installed via Gyan.FFmpeg winget package).

## Canonical CLI invocation

```bash
"C:\Users\A\Desktop\Autocrop-vertical\.venv\Scripts\python.exe" \
  "C:\Users\A\Desktop\Autocrop-vertical\main.py" \
  -i "<input.mp4>" \
  -o "<output_vertical.mp4>"
```

Output: 9:16 mp4 with subject tracked through scenes. Output height = source height (no upscaling).

## Common variants

```bash
# Instagram feed 4:5
... -i in.mp4 -o out.mp4 --ratio 4:5

# Square 1:1 for IG carousel
... -i in.mp4 -o out.mp4 --ratio 1:1

# High quality (CRF 18, slow preset) — final masters
... -i in.mp4 -o out.mp4 --quality high

# Fast preview encode (CRF 28, veryfast)
... -i in.mp4 -o out.mp4 --quality fast

# Dry-run: show the per-scene TRACK/LETTERBOX plan, no encode
... -i in.mp4 -o out.mp4 --plan-only

# NVIDIA NVENC hardware encode (auto-falls back to libx264 if unavailable)
... -i in.mp4 -o out.mp4 --encoder hw

# Faster scene detection on long videos (skip every other frame)
... -i in.mp4 -o out.mp4 --frame-skip 1
```

## Quality presets (libx264)

| `--quality` | CRF | x264 preset | Use for |
|-------------|-----|-------------|---------|
| `fast`      | 28  | veryfast    | Drafts, previews |
| `balanced`  | 23  | fast        | **Default — good for Shorts uploads** |
| `high`      | 18  | slow        | Master copies, archival |

## Pipeline integration — viral-clipper

In `viral-clipper`, after clip extraction and before the final ffmpeg render, branch:

1. Run `ffprobe` on the cut clip to get resolution.
2. If clip is already vertical (h > w) → skip, just normalize.
3. Else run a quick YOLO face-count: if `face_count <= 1` AND faces stay near horizontal-center (±15% of width) for >80% of the clip → use simple ffmpeg center-crop (faster).
4. Otherwise → call AutoCrop-Vertical with `--quality balanced --encoder hw`.

Result: Shorts where two-person interviews keep both heads in frame instead of chopping one off.

## Performance expectations (CPU torch, no NVIDIA acceleration)

YOLOv8n on CPU runs scene-middle inference in ~150-300 ms per scene. The dominant cost is PySceneDetect (~50% of total runtime) + libx264 encoding. Rough ranges on a typical laptop:

| Source | Approx runtime |
|--------|----------------|
| 720p, 60s | ~30-60 s |
| 1080p, 60s | ~60-120 s |
| 1080p, 12 min | 5-12 min |

If batch-processing many clips, `--encoder hw` (NVENC on the RTX 5080 laptop) can roughly halve total time at the encode stage.

## Verification (run once after install change)

```bash
"C:\Users\A\Desktop\Autocrop-vertical\.venv\Scripts\python.exe" \
  "C:\Users\A\Desktop\Autocrop-vertical\main.py" --help
```

Should print the usage block. If `torch` / `ultralytics` import fails, reinstall via:

```bash
"C:\Users\A\Desktop\Autocrop-vertical\.venv\Scripts\python.exe" -m pip install -r "C:\Users\A\Desktop\Autocrop-vertical\requirements.txt"
```

## Notes / gotchas

- **First run downloads `yolov8n.pt`** (~6 MB) into the repo root. Don't `git pull --rebase` and panic if you see this file uncommitted.
- **CPU torch 2.11.0 is intentional** — Python 3.14 has no torch wheels yet (as of 2026-05). The repo's `.venv` is locked to Python 3.12 via `py -3.12 -m venv`. Don't recreate it with the system Python.
- **Audio sync:** repo handles non-zero stream start_time and VFR sources automatically. Do not pre-process the input with ffmpeg "to be safe" — it can hurt sync.
- **Output extension:** if you omit `.mp4` from `-o`, it auto-appends.
- Repo URL: https://github.com/kamilstanuch/Autocrop-vertical
