---
name: video-use
description: Agentic NLE pattern — read raw footage as a transcript (NOT frames), produce an Edit Decision List (EDL), then emit ffmpeg/moviepy/Remotion render commands. Use when the user says "edit raw footage", "cut a video from transcript", "agentic video editing", "turn these takes into a video", "remove filler words / dead space / umms", "make a podcast cut from these clips", "talking-head trim", or drops a folder of MP4s/MOVs and asks for `final.mp4`. Adapted from browser-use/video-use prompt pattern (no code copied — repo is unlicensed). Wires into the author's existing skills rather than duplicating them.
---

# video-use — Agentic Video Editing

The LLM never WATCHES the footage. It READS it as a transcript with word-level timestamps, decides cuts at word boundaries, emits an EDL, then drives ffmpeg / moviepy / Remotion to render. Same trick as browser-use giving an LLM a structured DOM instead of a screenshot.

> 30k frames × 1.5k tokens = 45M tokens of noise. Transcript = ~12KB. Pick the cheap one.

## When to invoke

Trigger on any of:
- "edit these into a video / launch video / podcast cut / reel"
- "cut filler words / umms / false starts / dead space"
- "turn this raw footage into final.mp4"
- "agentic video editing"
- user drops a folder containing `*.mp4 / *.mov / *.mkv` and says "edit"

## Existing skills this orchestrates (DO NOT duplicate)

Invoke these by name via the `Skill` tool — never inline their content:

| Stage              | Skill                       | Use for                                                |
| ------------------ | --------------------------- | ------------------------------------------------------ |
| Transcribe         | `elevenlabs`                | Scribe word-level timestamps + diarization (preferred) |
| Transcribe (local) | (whisper.cpp / faster-whisper, no skill) | Offline fallback if ELEVENLABS_API_KEY missing |
| Trim / concat / encode | `ffmpeg`                | Cuts, concatenation, fades, color, subtitle burn-in    |
| Python composition | `moviepy`                   | Programmatic overlays, text burn-in, complex layouts   |
| React video        | `remotion` + `remotion-official` | Animated overlays, lower-thirds, intros/outros    |
| TTS / VO           | `elevenlabs`                | Re-voice, pickup lines, dub                            |
| Music              | `acestep`                   | Background music, stems                                |

If the user wants channel-style content (book breakdown, viral clip, demo), prefer the more specific skills (`channel-breakdown`, `viral-clipper`, `book-video`, `record-demo`, `video-edit`). This skill is for raw-footage agentic editing.

## The pipeline

```
Ingest --> Transcribe --> Pack --> Reason (EDL) --> Confirm --> Render --> Self-Eval --> (loop max 3) --> final.mp4
```

All outputs land in `<videos_dir>/edit/`. Source folder stays clean.

### 1. Ingest

```bash
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,duration \
        -show_entries format=duration -of json "<source>.mp4"
```
Record per source: path, duration, fps, resolution, audio sample rate, codec. Save to `edit/sources.json`.

### 2. Transcribe (Layer 1 — always loaded)

Default = ElevenLabs Scribe via the `elevenlabs` skill. Request:
- model: `scribe_v1`
- diarize: true
- audio events: true (laughter, applause, sigh)
- output: word-level timestamps

Save raw response to `edit/transcripts/<source>.json`.

### 3. Pack — `takes_packed.md`

Compress every transcript into ONE markdown file the LLM reads directly. Keep under ~15KB total.

```
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
  [007.20-009.10] S0 (sigh) Umm, so what we did was--
  [010.40-013.95] S0 We rebuilt the whole transcript layer.
```

This is the LLM's primary editing surface. Word timestamps live in the JSON; phrases in the .md.

### 4. Reason — produce an EDL

The LLM reads `takes_packed.md` and emits an Edit Decision List. JSON schema:

```json
{
  "fps": 30,
  "resolution": [1920, 1080],
  "segments": [
    {"src": "C0103.mp4", "in": 2.52, "out": 5.36, "speaker": "S0", "transition": "cut"},
    {"src": "C0103.mp4", "in": 6.08, "out": 6.74, "speaker": "S0", "transition": "cut"},
    {"src": "C0107.mp4", "in": 11.20, "out": 24.80, "speaker": "S0", "transition": "crossfade:0.4"}
  ],
  "audio_fade_ms": 30,
  "subtitles": {"style": "2word_upper", "burn": true},
  "color": "warm_cinematic"
}
```

Hard rules (non-negotiable):
1. Cuts at word boundaries only. Never mid-word.
2. 30ms audio fade at every cut to kill pops.
3. Drop `umm`, `uh`, `like` (filler) and false starts unless speaker corrects them mid-thought.
4. Drop dead space > 600ms.
5. Never assume content type — infer it, then ASK the user before cutting.
6. EDL is reviewed before render. No cuts without strategy approval.

### 5. Confirm

Show the user: source inventory, proposed strategy in 4 bullets, EDL summary (segment count + total duration). Wait for "go" before rendering.

### 6. Render

Pick the engine that fits:

**ffmpeg (default — fastest)** — invoke the `ffmpeg` skill. Pattern:
```bash
# Trim each segment to a temp file
ffmpeg -i C0103.mp4 -ss 2.52 -to 5.36 -af "afade=in:st=2.52:d=0.03,afade=out:st=5.33:d=0.03" -c:v libx264 -crf 18 seg_001.mp4
# Concat
ffmpeg -f concat -safe 0 -i list.txt -c copy edit/final_raw.mp4
# Burn subs + color
ffmpeg -i edit/final_raw.mp4 -vf "subtitles=edit/subs.ass,eq=contrast=1.05:saturation=1.1" edit/final.mp4
```

**moviepy (when programmatic overlays needed)** — invoke `moviepy` skill. Use for: animated text, transparent PNG overlays, anything with PIL composition.

**Remotion (when animated motion graphics)** — invoke `remotion` + `remotion-official`. Use for: lower-thirds, intros, kinetic-typography sections. Output an MP4, then concat into the ffmpeg pipeline.

### 7. Self-Eval (loop, max 3)

After each render, run `ffmpeg -ss <cut_t-0.2> -to <cut_t+0.2>` at every cut boundary, dump 3 frames, inspect:
- visual jump cut artifact?
- audio pop / click?
- subtitle overlapping speaker face / cropped?
- color banding at transition?

If any issue: patch EDL → re-render that segment only → re-check. Bail at 3 iterations and surface to the user.

### 8. Persist

Write `edit/project.md` with: source list, EDL, render settings, eval notes. Next session resumes from this file.

---

## Worked example 1 — Talking-head trim

User drops `~/Desktop/launch_takes/` with 3 mp4s (8 min total) and says "edit these into a 90-second launch clip".

1. ffprobe each → `edit/sources.json` (3 files, 1080p30, 8m07s combined).
2. Skill `elevenlabs` Scribe → 3 JSON transcripts.
3. Pack → `takes_packed.md` (4 KB, 47 phrases).
4. Read packed.md, cut 11 fillers + 4 false starts + 6 dead-air gaps, pick the strongest 14 phrases. Emit EDL targeting 88-92s.
5. Show the user: "3 sources -> 14 segments -> 89s. Warm color, 2-word UPPERCASE subs, 30ms fades. Render?"
6. On "go", run `ffmpeg` skill: trim 14 segments, concat, burn subs, grade. → `edit/final.mp4`.
7. Self-eval each of 13 cut boundaries. Detect 1 audio pop at cut 7 → fix afade timing → re-render seg 7 only → re-concat. Pass.
8. Persist `edit/project.md`.

## Worked example 2 — Multi-clip podcast cut

User drops `~/Desktop/podcast_ep04/` with 4 mp4s (host cam, guest cam, screen share, room mic) totaling 1h12m. "Cut this into a 25-min episode, drop tangents, keep the AI ethics segment."

1. ffprobe all 4. Identify the room mic as primary audio source (host cam audio worse).
2. `elevenlabs` Scribe on room mic only (one transcript covers both speakers via diarization).
3. Pack → `takes_packed.md` (~14 KB).
4. Read packed.md, identify "AI ethics" topic windows by content, drop the 22-min food tangent + 7 min of equipment talk. Build EDL with cam switching: default to whoever is speaking (S0=host cam, S1=guest cam), cut to screen share when terms get technical.
5. Show the user the topic map + segment count + final duration estimate. Confirm.
6. Render via `ffmpeg`: per-segment trim of room mic + appropriate cam, concat with 30ms fades, burn lower-thirds via `remotion` for chapter markers, mux room mic on top of all video segments (single clean audio bed).
7. Self-eval at each cam switch — check for sync drift, audio level jumps. Fix and re-render hot spots.
8. `edit/final.mp4` + `edit/project.md`.

---

## Anti-patterns (do NOT)

- Do NOT dump frames into the LLM context. The transcript is the surface.
- Do NOT cut without the author's "go" on the strategy.
- Do NOT skip the 30ms fade — every cut without it pops.
- Do NOT use square 1:1 output — match the source aspect or 16:9 / 9:16 as requested.
- Do NOT overwrite source files. All output → `edit/`.
- Do NOT clone the browser-use/video-use repo. It has no license. Pattern only.

## Verification before claiming done (golden rule applies)

Per `~/.claude/CLAUDE.md` rule #1: don't say "done" until `edit/final.mp4` exists, plays end-to-end, passes self-eval at every cut boundary, and matches the agreed duration ±2s. Show the user the file path and the duration.
