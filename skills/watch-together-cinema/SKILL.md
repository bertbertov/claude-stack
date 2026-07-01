---
name: watch-together-cinema
description: Build a private, self-hosted "watch a movie together in sync" site for two people in different countries — synced play/pause/seek over WebSocket, WebRTC camera+mic call with a coturn TURN relay, a shared laser pointer, ffmpeg smooth-bitrate transcoding so it never buffers, and a token-gated room link. Use when someone wants to watch local video files in sync with a partner/friend remotely, replace Kosmi/Teleparty/Twoseven with something they own, stream a personal movie library over the web with synced controls, or add a video-call overlay to a video player. Triggers: "watch movies together long distance", "sync video playback two browsers", "self-hosted watch party", "Kosmi alternative", "stream my movie to my girlfriend with subtitles and sync".
---

# Watch-Together Cinema

A private cinema you own: upload a movie, get an unguessable room link, send it to one other person, and you both watch **in sync** (either side controls play/pause/seek) with an optional **camera+mic call** overlaid and a **shared laser pointer**. No Kosmi/Teleparty subscription, no per-message limits, no sending big files around.

Reference implementation lives in `reference/` — a ~180-line FastAPI backend, a YouTube-style player, an admin page, plus nginx + coturn examples. Copy them, fill placeholders, deploy.

## Architecture (the important distinction)

There are two separable problems and only one is hard:
- **Sync** (mirror play/pause/seek between two browsers) — trivial: a WebSocket relay.
- **Delivering the video** — the real work. You serve the file over HTTP with byte-range (so seeking works) directly from the host.

```
browser A ─┐                         ┌─ nginx :443 (TLS)
           ├── wss sync + signaling ──┤    ├── /media/*  → static file, byte-range (video)
browser B ─┘                         │    └── /        → uvicorn :8088 (FastAPI: pages, upload, WS)
                                     └─ coturn :3478   → WebRTC relay (camera/mic, NAT fallback)
```

- **Movie stream:** peer downloads the file from *your* server. One viewer = trivial bandwidth.
- **Camera call:** WebRTC **peer-to-peer** (cameras go directly between the two browsers). The WebSocket doubles as the signaling channel; **coturn** relays only when NAT/CGNAT blocks a direct path (common on mobile/home ISPs across countries).

## Components (in `reference/`)

| File | What it is |
|---|---|
| `app.py` | FastAPI: token-gated watch rooms, key-gated admin upload/list/delete, WebSocket that relays sync + WebRTC signaling + pointer, ffmpeg faststart-remux + `.srt`→`.vtt` on upload. Serves video via `StaticFiles` (byte-range capable). Admin key from `CINEMA_ADMIN_KEY` env — no hardcoded secrets. |
| `player.html` | The watch room. Custom YouTube-style controls (auto-hide, scrub bar), keyboard (Space/K play, ←/→ 5s, J/L 10s, ↑/↓ volume, M mute, C subs, F fullscreen, P pointer), buffer-aware drift-correction sync, WebRTC call with draggable/resizable tiles, shared laser pointer. Has `{{TURN_HOST}}` / `{{TURN_USER}}` / `{{TURN_PASS}}` placeholders — fill before serving. |
| `admin.html` | Upload (movie + optional subtitles) with progress, list, copy room link, delete. Key comes from `?key=` in the URL. |
| `nginx.conf.example` | Reverse proxy: serves `/media/` statically (native range), proxies everything else + WebSocket upgrade to uvicorn, `client_max_body_size 0` for multi-GB uploads. |
| `turnserver.conf.example` | coturn config (long-term credential, relay port range, external-ip). |

## Deploy (once)

1. **Server + Python:**
   ```bash
   mkdir -p /opt/cinema/media /opt/cinema/static
   python3 -m venv /opt/cinema/venv
   /opt/cinema/venv/bin/pip install fastapi "uvicorn[standard]" python-multipart websockets
   cp reference/app.py /opt/cinema/app.py
   cp reference/player.html reference/admin.html /opt/cinema/static/
   apt-get install -y ffmpeg    # for faststart remux + srt→vtt
   ```
2. **Admin key** (systemd unit):
   ```ini
   # /etc/systemd/system/cinema.service
   [Service]
   Environment=CINEMA_ADMIN_KEY=%GENERATE_A_RANDOM_HEX%   # openssl rand -hex 12
   WorkingDirectory=/opt/cinema
   ExecStart=/opt/cinema/venv/bin/uvicorn app:app --host 0.0.0.0 --port 8088
   Restart=always
   [Install]
   WantedBy=multi-user.target
   ```
   `systemctl enable --now cinema`
3. **Domain + TLS.** Point a subdomain straight at the host (**A record, DNS-only** if behind Cloudflare — CF's free plan caps uploads at 100 MB and restricts video, so the media path MUST bypass the proxy). Then `certbot --nginx -d cinema.example.com` with `nginx.conf.example`.
4. **TURN (coturn)** for the camera call to survive cross-country NAT:
   ```bash
   apt-get install -y coturn
   cp reference/turnserver.conf.example /etc/turnserver.conf   # set your own user:password, realm, external-ip
   sed -i 's/#TURNSERVER_ENABLED=1/TURNSERVER_ENABLED=1/' /etc/default/coturn
   systemctl enable --now coturn
   ```
   Put the same TURN host/user/password into `player.html`'s `{{TURN_*}}` placeholders. Verify the relay actually works: `turnutils_uclient -y -u USER -w PASS -n 4 YOUR_HOST` should report `Total lost packets 0`.

## Use

- Admin: `https://cinema.example.com/admin?key=YOUR_ADMIN_KEY` → upload movie (+ `.srt`) → wait for **ready** → copy the room link.
- Send the room link to the other person. Both open it → **Start watching together** → synced. Press **P** and move the mouse for the shared pointer. Click the call icon to turn on cameras (earbuds recommended — speakers + open mic = echo).

## The buffering fix (this is the #1 real-world problem)

Movies are usually **VBR** — a file that averages ~2 Mbit/s spikes to ~10 Mbit/s on busy scenes. While a camera call also runs, those spikes outrun a home/mobile connection and the movie stutters. **Fix: transcode to a capped constant bitrate before uploading** (no spikes, visually identical). On a machine with an NVIDIA GPU:

```bash
ffmpeg -i input.mp4 -map 0:v:0 -map 0:a:0 \
  -c:v h264_nvenc -preset p5 -rc vbr -b:v 2500k -maxrate 3000k -bufsize 6000k \
  -profile:v high -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart output.mp4
# CPU-only: swap -c:v h264_nvenc ... for -c:v libx264 -crf 21 -maxrate 3000k -bufsize 6000k
```

Extract embedded subtitles to upload alongside: `ffmpeg -i input.mp4 -map 0:s:0 subs.srt`

Do heavy transcodes on a GPU box (minutes), not a CPU-only VPS (hours). The app's on-upload step only does a fast **stream-copy faststart remux** (`-c copy -movflags +faststart`) — instant for already-H.264/AAC MP4s — plus `.srt`→`.vtt`.

## Design notes worth keeping

- **Sync is buffer-aware.** Don't hard-seek on small drift (causes visible skipping). Only seek when drift > ~3s (someone scrubbed); for smaller drift the *behind* side nudges `playbackRate` to 1.04 to glide back. Suppress state broadcasts while `buffering`, so a stalled peer doesn't drag the other backward.
- **Fullscreen the wrapper, not the `<video>`.** Native video-fullscreen hides sibling elements — so the camera tiles and pointer vanish. Call `requestFullscreen()` on the container that holds video + tiles + pointer layer.
- **Cap the call bitrate** (`sender.setParameters` `maxBitrate ~400 kbps`, 360p/20fps) so the call never starves the movie stream.
- **Privacy:** room tokens and media filenames are unguessable random hex; admin is key-gated; pages carry `noindex`. It's private-by-obscurity for two people — fine for personal use, not a public multi-tenant service.
- **Codec:** browsers only reliably play **MP4 / H.264 / AAC**. MKV/HEVC/AC3 must be transcoded (the capped-bitrate command above also fixes codec).

## When NOT to use

- More than a handful of simultaneous viewers, or a public audience → use a real streaming/CDN stack, not this.
- You don't control a server with a domain → use Syncplay (each person keeps their own file copy) or a hosted watch-party service.
