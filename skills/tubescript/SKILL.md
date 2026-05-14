---
name: tubescript
description: Speaker diarization (who-spoke-when labels) + Whisper transcription for podcasts, interviews, multi-person videos, and YouTube URLs. Use when the user asks any of - "who's speaking when", "diarize this podcast", "speaker labels for video", "label speakers in interview", "split podcast by speaker", "transcribe with speaker names", "label this conversation". Local install at C:\Users\A\Desktop\TubeScript\ — pyannote.audio 3.1 + OpenAI Whisper + FastAPI backend + Vite frontend, exports SRT/VTT/TXT with speaker tags.
---

# TubeScript — Speaker Diarization + Transcription

Local pipeline that ingests a YouTube URL (or batches of them), splits audio by speaker using pyannote.audio 3.1, transcribes each segment with Whisper, and exports speaker-labeled transcripts as SRT / VTT / TXT.

This is the **missing layer** for multi-speaker editing — the existing `/youtube-transcripts` skill only pulls YouTube's built-in captions (one block of text, no speaker labels). TubeScript answers "who said what when" so the output can be fed into:

- `/channel-breakdown` — pull quotes attributed to a specific guest in a podcast appearance
- `/viral-clipper` — auto-cut clips that contain only one speaker's segments
- `/transcript-analyzer` — extract decisions/action items per speaker
- General podcast/interview content where guest vs host attribution matters

---

## Install location

| Path | What |
| --- | --- |
| `C:\Users\A\Desktop\TubeScript\` | Repo root (cloned from github.com/Davenads/TubeScript) |
| `C:\Users\A\Desktop\TubeScript\backend\` | FastAPI + pipeline code |
| `C:\Users\A\Desktop\TubeScript\backend\venv\` | **Python 3.12** venv (NOT 3.14 — pyannote/torch/whisper not 3.14-ready yet) |
| `C:\Users\A\Desktop\TubeScript\backend\venv\Scripts\python.exe` | Python interpreter to invoke for everything |
| `C:\Users\A\Desktop\TubeScript\backend\.env` | Holds `HUGGINGFACE_TOKEN=...` (you create this) |
| `C:\Users\A\Desktop\TubeScript\frontend\` | Vite/React UI (optional — backend-only flow works too) |
| `C:\Users\A\Desktop\TubeScript\start.bat` | One-shot launcher (backend + frontend windows) |

> Note: README/start.bat both expect the venv at `backend\venv\` (NOT `repo\.venv\`). Stick with that — the launcher script depends on it.

---

## One-time setup

### 1. HuggingFace token (REQUIRED — pyannote models are gated)

1. Sign in at https://huggingface.co
2. Accept terms of use on BOTH model pages (one click each):
   - https://huggingface.co/pyannote/speaker-diarization-3.1
   - https://huggingface.co/pyannote/segmentation-3.0
3. Create a token at https://huggingface.co/settings/tokens (Read scope is enough)
4. Drop it into `C:\Users\A\Desktop\TubeScript\backend\.env`:

   ```
   HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxx
   ```

Without all three steps, diarization throws `gated repo` and falls over. Whisper does NOT need a token.

### 2. FFmpeg on PATH

`yt-dlp` and `whisper` both shell out to ffmpeg. Verify with `ffmpeg -version`. If missing, install via `winget install ffmpeg` or drop a static build into a PATH dir.

### 3. First-run model preload (downloads ~3-5 GB)

```bash
"C:\Users\A\Desktop\TubeScript\backend\venv\Scripts\python.exe" "C:\Users\A\Desktop\TubeScript\backend\preload_models.py"
```

Pulls Whisper `large` (~3 GB) + pyannote diarization-3.1 (~500 MB) into HF cache. Skip and they'll lazy-download on first job — preloading just makes the first transcription not stall for 5 minutes.

### 4. Frontend deps (only if you want the web UI)

```bash
cd C:\Users\A\Desktop\TubeScript\frontend
npm install
```

---

## Running it

### Option A — full stack via launcher (recommended)

```bat
C:\Users\A\Desktop\TubeScript\start.bat
```

Opens:
- Backend FastAPI → http://localhost:8001
- Frontend Vite UI → http://localhost:3000

Paste a YouTube URL into the UI, set diarization sensitivity (0.5 default = looser, 0.7+ = more speakers detected), wait, then rename SPEAKER_00 / SPEAKER_01 / ... to real names and export SRT/VTT/TXT.

### Option B — backend only (script the API)

```bash
"C:\Users\A\Desktop\TubeScript\backend\venv\Scripts\python.exe" "C:\Users\A\Desktop\TubeScript\backend\app.py"
```

Then POST to the API:

```bash
# Single video
curl -X POST http://localhost:8001/api/process \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtu.be/VIDEO_ID", "diarization_enabled": true, "diarization_sensitivity": 0.5}'

# → returns {"job_id": "...", "status": "queued"}

# Poll status
curl http://localhost:8001/api/status/<job_id>

# Get transcript
curl http://localhost:8001/api/transcript/<job_id>

# Export
curl http://localhost:8001/api/export/<job_id>?format=srt -o out.srt
curl http://localhost:8001/api/export/<job_id>?format=vtt -o out.vtt
curl http://localhost:8001/api/export/<job_id>?format=txt -o out.txt
```

Batch (whole playlist or recent channel videos): `POST /api/batch-process` with `{"url": "...", "limit": 10}`. See `BATCH_PROCESSING.md` in the repo.

### Option C — feed a local audio/video file (not a YouTube URL)

The repo's public API only takes YouTube URLs. To diarize a local file, call the modules directly:

```python
import asyncio
from modules.diarization import perform_diarization
from modules.transcription import transcribe_segments
from modules.assembler import assemble_transcript

async def main():
    diarization = await perform_diarization("C:/path/to/audio.wav", sensitivity=0.5)
    segments = await transcribe_segments("C:/path/to/audio.wav", diarization)
    transcript = assemble_transcript(segments)
    print(transcript)

asyncio.run(main())
```

Run inside the venv from `backend/` so the `modules.*` imports resolve.

---

## Output formats

All three carry speaker labels:

- **SRT** — `[SPEAKER_00] Hello there.` inside subtitle blocks. Drop into Premiere/DaVinci.
- **VTT** — same, WebVTT cue format. Drop into HTML5 `<track>`.
- **TXT** — `SPEAKER_00 [00:01:23]: Hello there.` blocks. Best for feeding into LLMs / `/transcript-analyzer`.

Rename `SPEAKER_00` → real name via `POST /api/rename/<job_id>` BEFORE exporting (mapping persists for that job).

---

## Hardware

- **GPU strongly recommended.** Repo says NVIDIA RTX 4070 Super or better. CPU works but a 30-min podcast takes ~hours instead of minutes.
- VRAM: ~6 GB for Whisper large + pyannote loaded simultaneously.
- Use `whisper.load_model("medium")` instead of `large` (edit `backend/modules/transcription.py`) if VRAM-constrained — quality tradeoff is small for English.

---

## Tuning

| Knob | Where | Effect |
| --- | --- | --- |
| `diarization_sensitivity` | API param 0.0–1.0 | Higher → detects more speakers (and more false positives) |
| Whisper model size | `transcription.py` (`tiny/base/small/medium/large`) | Bigger = slower but more accurate. `large` is the default. |
| Min speaker duration | pyannote pipeline params | Filters out quick interjections labeled as separate speakers |

For interviews with 2 people: leave defaults at 0.5.
For panel discussions (4+ speakers): bump to 0.65–0.75.
For monologue with occasional guest: drop to 0.3 to suppress over-segmentation.

---

## KNOWN ISSUES from initial install (2026-05-07)

These were observed on this machine after running `pip install -r requirements.txt`. Fix BEFORE first run.

### Issue 1: torch installed CPU-only (no CUDA acceleration)

`pip install torch>=2.0.0` from the loose requirement pulls CPU wheels by default on Windows. Verify:

```bash
"C:\Users\A\Desktop\TubeScript\backend\venv\Scripts\python.exe" -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# If output ends with "False" → CPU only, transcription will be brutally slow
```

**Fix** — reinstall torch with the CUDA 12.1 wheels (matches the 50-series + 4070 super):

```bash
"C:\Users\A\Desktop\TubeScript\backend\venv\Scripts\python.exe" -m pip uninstall -y torch torchaudio torchvision torchcodec
"C:\Users\A\Desktop\TubeScript\backend\venv\Scripts\python.exe" -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Issue 2: `pyannote.audio 4.0.4` installed (not 3.x as repo expects)

The requirements pin `pyannote.audio>=2.1.1` so pip resolves to current 4.0.x. Repo code references `pyannote/speaker-diarization-3.1` model which still loads, BUT 4.0 introduced the `torchcodec` dependency that fails to load on Windows without ffmpeg DLLs visible to the linker. You'll see a wall of `Could not find libtorchcodec_coreN.dll` warnings on import.

**Workarounds (pick one):**
- Pin to last 3.x: `pip install "pyannote.audio>=3.1,<4.0"`
- Or install the FULL ffmpeg "shared" build (DLLs, not just the .exe) and add the bin dir to PATH. The "essentials" winget build is exe-only.
- Or feed audio as preloaded `{"waveform": tensor, "sample_rate": int}` dicts (the warning text suggests this).

The warnings are non-fatal IF you only use the YouTube path (yt-dlp downloads to wav, then pyannote reads the wav via its non-torchcodec fallback). They become fatal if you call `Pipeline(...)` on a video file directly.

### Issue 3: Python 3.14 incompatible

Global Python on this box is 3.14, but `pyannote.audio` and `whisper` have no 3.14 wheels yet. Install was forced to Python 3.12 via `py -3.12 -m venv ...`. If you ever recreate the venv, use `py -3.12`, NOT plain `python`.

---

## Common failure modes

| Symptom | Fix |
| --- | --- |
| `gated repo` / 401 from pyannote | Forgot to accept terms on the two HF model pages — see Setup §1 |
| `HUGGINGFACE_TOKEN not found` | `.env` missing or backend started outside `backend/` directory (dotenv looks at cwd) |
| `CUDA not available, using CPU` warning | See KNOWN ISSUE 1 above — reinstall torch with cu121 wheels |
| `Could not load libtorchcodec_core*.dll` | See KNOWN ISSUE 2 above — pin pyannote.audio<4.0 OR install full-shared ffmpeg |
| `ffmpeg: command not found` (during yt-dlp) | Install ffmpeg, restart shell |
| Frontend ports clash | start.bat says backend=8001, frontend=3000 in the echo but README says 8000/5173. Check `start.bat` and `frontend/vite.config.js` for actual ports — start.bat is authoritative |
| All speakers labeled SPEAKER_00 | Sensitivity too low, or audio is genuinely single-speaker, or the two voices are too similar (same gender + similar pitch + bad mic). Try sensitivity 0.7+ |

---

## Integration cheatsheet

```text
YouTube interview URL
    │
    ▼
[ TubeScript ]  ── speaker-labeled SRT/TXT
    │
    ├──► /transcript-analyzer  → "what did the guest claim about X"
    ├──► /viral-clipper        → cut only guest's punchy lines
    └──► /channel-breakdown    → quote-attribution in essay videos
```

The whole point: anywhere the existing transcript pipeline drops "wall of text with no attribution," TubeScript replaces it with "labeled dialogue you can route per-speaker."
