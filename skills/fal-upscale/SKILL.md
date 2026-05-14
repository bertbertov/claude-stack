---
name: fal-upscale
description: AI video upscaling via fal.ai (Topaz, ByteDance, Wan Vision Enhancer) — take 768px / 720p clips up to 1080p or 4K for YouTube. Use when upscaling video, cleaning up rendered AI video, taking ltx2 output to 4K, or preparing footage for high-resolution delivery. Triggers include "upscale video", "make this 4K", "ltx2 output looks blurry", "clean up rendered video", "1080p upscale", "topaz upscale", "video super resolution".
---

# fal.ai Video Upscale

Upscale low-res video (e.g. ltx2's 768px output, 720p AI clips, old footage) to 1080p or 4K using fal.ai's hosted upscalers. Designed to bolt onto the ltx2 pipeline so generated clips ship YouTube-ready.

## When to use which model

| Endpoint                             | Best for                                       | Notes |
|--------------------------------------|------------------------------------------------|-------|
| `fal-ai/topaz/upscale/video`         | **Default.** Polished pro-grade upscale.       | The standard. Topaz Video AI under the hood. |
| `fal-ai/bytedance-upscaler/upscale/video` | Cheaper alternative, faster turnarounds.   | Use when Topaz cost stings on long clips. |
| `fal-ai/wan-vision-enhancer`         | Wan-family AI clips, restoration + enhance.    | Vision enhancement, not pure upscale. |

> **AuraSR (`fal-ai/aura-sr`) is image-only.** Don't try it on video — use Topaz for video.

## Auth

1. Grab a key from https://fal.ai/dashboard/keys
2. Set the env var:

```bash
# bash / zsh / WSL
export FAL_KEY="fal_xxxxxxxxxxxxxxxx"

# Windows PowerShell (persistent)
[Environment]::SetEnvironmentVariable("FAL_KEY", "fal_xxx...", "User")

# Windows cmd (current shell)
set FAL_KEY=fal_xxxxxxxxxxxxxxxx
```

The `fal_client` library auto-picks up `FAL_KEY` from the environment.

## Install

```bash
pip install fal-client
```

## Pricing (Topaz, as of 2026)

| Output resolution | Price per second of video |
|-------------------|---------------------------|
| up to 720p        | $0.01 / sec               |
| 720p → 1080p      | $0.02 / sec               |
| above 1080p (4K)  | $0.08 / sec               |

- **60fps output → price doubles.**
- **Gaia 2 model output → half price.**
- Rough rule: a 5-sec ltx2 clip → 1080p ≈ **$0.10**, → 4K ≈ **$0.40**.
- AuraSR (image only) is the cheapest tier at $0.001/compute-sec but doesn't apply here.

## Canonical workflow: ltx2 → upscale → download

ltx2 generates a local `.mp4` at 768px → upload to fal storage → Topaz upscales → download the result.

```python
import fal_client
import urllib.request
from pathlib import Path

LOCAL_CLIP = Path("ltx2_out/sunset.mp4")     # the 768px clip from ltx2
TARGET     = Path("ltx2_out/sunset_4k.mp4")

# 1. Upload the local clip to fal storage → returns a public URL
video_url = fal_client.upload_file(str(LOCAL_CLIP))
print(f"uploaded: {video_url}")

# 2. Run Topaz upscale (subscribe = blocks + polls automatically)
def on_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs or []:
            print(log["message"])

result = fal_client.subscribe(
    "fal-ai/topaz/upscale/video",
    arguments={
        "video_url": video_url,
        # Optional knobs (see schema):
        # "target_fps": 30,           # frame interpolation
        # "upscale_factor": 2,        # 2x or 4x
        # "H264_output": True,        # mp4 instead of mov
    },
    with_logs=True,
    on_queue_update=on_update,
)

# 3. Download the upscaled mp4
out_url = result["video"]["url"]
urllib.request.urlretrieve(out_url, TARGET)
print(f"saved: {TARGET}  ({result['video'].get('file_size', '?')} bytes)")
```

## CLI one-liner (quick test)

```bash
python -c "import fal_client; r = fal_client.subscribe('fal-ai/topaz/upscale/video', arguments={'video_url': 'https://example.com/clip.mp4'}, with_logs=True); print(r['video']['url'])"
```

## Inspecting the schema

Don't guess args — pull the live schema:

```bash
# If fal-models-catalog / genmedia is installed:
genmedia schema --endpoint_id fal-ai/topaz/upscale/video

# Or just read it on the model page:
# https://fal.ai/models/fal-ai/topaz/upscale/video
```

## Common gotchas

- **`fal_client.subscribe()` blocks** until the job finishes. For batch (>10 clips) use `fal_client.submit()` + poll, or a `concurrent.futures` pool.
- **Long videos = real money.** Always run a 1-second smoke test first.
- **Output format:** Topaz returns `result["video"]["url"]` (mp4 by default). Other upscalers may use `result["video_url"]` — check the schema.
- **60fps doubles cost.** Only set `target_fps: 60` if you actually need it for slow-mo or motion-smooth delivery.
- **Above 1080p is 4× the 1080p price.** If YouTube 1440p is acceptable, save $0.06/sec by capping at 1080p and letting YouTube re-encode.
- **Verify end-to-end before claiming done:** check that `TARGET` exists on disk AND probe its resolution with `ffprobe -v error -select_streams v:0 -show_entries stream=width,height TARGET`. "Subscribe returned" is not verification — see global golden rule.

## Cost guardrail snippet

Drop this in any batch script to refuse runaway bills:

```python
def estimate_cost(seconds: float, target_res: str = "1080p", fps: int = 30) -> float:
    rates = {"720p": 0.01, "1080p": 0.02, "4k": 0.08}
    cost = seconds * rates[target_res]
    if fps == 60:
        cost *= 2
    return cost

assert estimate_cost(total_seconds, "4k", 30) < 5.00, "abort: would spend >$5"
```

## Related skills

- `ltx2` — generates the 768px source clips this skill upscales.
- `moviepy` / `ffmpeg` — for trimming, concat, and final mux after upscale.
- `prompt-videos` — prompt patterns for the upstream ltx2 generation.
