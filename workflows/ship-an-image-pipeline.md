# Workflow: ship an image generation pipeline

Generating consistent, on-brand images at scale via Replicate / fal.ai / local Flux.

## The prompt to use

```
Build an image pipeline for <USE CASE>.

Volume: <one-off | 10s/month | 100s/month | 1000s/month>
Style: <photographic / editorial / illustrated / brand-locked>
Subject types: <products / portraits / scenes / abstract>
Where outputs go: <social media / website hero / book covers / app assets>
Budget: <how much per month is OK>
```

## Routing by volume

| Volume | Best path | Why |
|--------|-----------|-----|
| One-off, < 5/month | fal.ai web playground | Zero setup |
| 10-100/month, varied | prompt-images skill + fal MCP | Tool-calls from chat |
| 100-1000/month, brand-locked | Custom pipeline: Flux LoRA + PIL composite | Consistent quality at scale |
| 1000s/month, all same | Replicate API + queue | Cheap per-image, async |

## Model picks by need

| Need | Model | URL | Price |
|------|-------|-----|-------|
| Premium photorealistic | Flux 2 Pro | fal.ai/models/fal-ai/flux-2-pro | $0.03/MP |
| Text on image (readable) | Nano Banana 2 (Gemini 3 Pro Image) | fal.ai/models/fal-ai/nano-banana-2 | $0.08/img |
| Identity-preserving edits | Nano Banana 2 (edit mode) | same | $0.08/img |
| Open-source local (free) | Flux Krea Dev FP8 via ComfyUI | local | $0 |
| Multi-image transformations | Qwen Image Edit Plus | fal.ai/models/fal-ai/qwen-image-edit-plus | $0.03/MP |
| Inpaint / fill | Flux Fill | local or fal | $0.05/MP |
| Style transfer / painterly | Seedream 4 | fal.ai | $0.03/img |

## Prompting (per prompt-images skill)

- **One subject, one verb, one setting.** Stack adjectives at the end.
- **Cinematic language beats stock-photo language.** "Photographed by Annie Leibovitz" > "professional photo"
- **Negative space matters.** Specify "with negative space on right for text overlay" if compositing
- **Aspect ratio drives composition.** 1:1 = symmetric, 3:4 = portrait-driven, 16:9 = scene-driven
- **Seed for consistency.** Lock the seed when iterating one image; randomize for variety

## Brand consistency

If you're generating 100+ images for the same brand:

1. **Train a Flux LoRA** on 20-50 reference images. Cost: ~$10 one-time on Replicate.
2. **Generate via your LoRA** as the base. Cost: ~$0.04/img on Replicate.
3. **Composite with PIL** (Python Pillow) for fixed brand header / footer / typography.

The `super-book-cover` skill (in this stack) documents this pattern for book covers. Same approach works for any brand asset.

## Cost rules of thumb

- Image: $0.03-0.08/each
- Video 5s 1080p: $0.20-1.00 depending on model
- Lip sync 5s: $0.07-0.50 depending on model
- Set fal wallet spend cap at $50/mo as safety belt

## Skills involved

- prompt-images, prompt-videos (Replicate prompting)
- find-models, run-models, compare-models (Replicate discovery + invocation)
- qwen-edit, gpt-image-2 (specific model wrappers)
- ffmpeg, moviepy (post-processing)
- frontendwebsiteimageskill (when generating for website use)
