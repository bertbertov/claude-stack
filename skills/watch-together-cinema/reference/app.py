#!/usr/bin/env python3
# cinema — private synced movie-watching for 2.
# FastAPI: admin upload/list/delete (key-gated) + token-gated watch rooms +
# WebSocket play/pause/seek sync + ffmpeg faststart-remux & srt->vtt on upload.
# Serves video with HTTP range (StaticFiles) so seeking works. Runs on :8088.
import os, json, secrets, asyncio
from pathlib import Path
from fastapi import FastAPI, UploadFile, Form, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path('/opt/cinema')
MEDIA = ROOT / 'media'
STATIC = ROOT / 'static'
REG = ROOT / 'movies.json'
ADMIN_KEY = os.environ.get('CINEMA_ADMIN_KEY', 'changeme')
MEDIA.mkdir(parents=True, exist_ok=True)

def load_reg():
    try:
        return json.loads(REG.read_text())
    except Exception:
        return {}

def save_reg(r):
    REG.write_text(json.dumps(r, indent=2))

app = FastAPI(title='cinema')
app.mount('/media', StaticFiles(directory=str(MEDIA)), name='media')  # Range-capable

rooms = {}  # room_token -> {'state': {paused,time} | None, 'clients': set()}

def check_key(key):
    if not secrets.compare_digest(str(key), ADMIN_KEY):
        raise HTTPException(403, 'bad admin key')

@app.get('/', response_class=HTMLResponse)
def home():
    return '<body style="background:#0a0a0b;color:#a1a1aa;font-family:system-ui;padding:3rem">' \
           '<h1 style="color:#fafafa">cinema</h1><p>private. nothing to see here.</p></body>'

@app.get('/admin', response_class=HTMLResponse)
def admin_page(key: str = ''):
    check_key(key)
    return (STATIC / 'admin.html').read_text(encoding='utf-8')

@app.get('/api/list')
def api_list(key: str = ''):
    check_key(key)
    r = load_reg()
    return [{'id': k, 'title': v['title'], 'status': v['status'],
             'room': v['room'], 'has_subs': bool(v.get('vtt'))} for k, v in sorted(r.items(), key=lambda kv: kv[1].get('ts',0), reverse=True)]

@app.post('/api/upload')
async def api_upload(key: str = Form(...), title: str = Form(...),
                     movie: UploadFile = None, subs: UploadFile = None):
    check_key(key)
    if movie is None:
        raise HTTPException(400, 'no movie file')
    mid = secrets.token_hex(8)
    raw = MEDIA / f'{mid}.raw'
    with raw.open('wb') as f:
        while True:
            chunk = await movie.read(4 * 1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    sub_raw = None
    if subs is not None and subs.filename:
        sub_raw = MEDIA / f'{mid}.srt'
        with sub_raw.open('wb') as f:
            while True:
                chunk = await subs.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
    r = load_reg()
    import time as _t
    r[mid] = {'title': title, 'file': f'{mid}.mp4', 'vtt': None,
              'room': secrets.token_urlsafe(9), 'status': 'processing', 'ts': int(_t.time())}
    save_reg(r)
    asyncio.create_task(process(mid, raw, sub_raw))
    return {'id': mid, 'room': r[mid]['room'], 'status': 'processing'}

async def _run(*args):
    p = await asyncio.create_subprocess_exec(*args,
        stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
    _, err = await p.communicate()
    return p.returncode, (err or b'').decode('utf-8', 'ignore')[-400:]

async def process(mid, raw, sub_raw):
    out = MEDIA / f'{mid}.mp4'
    # 1) try fast stream-copy remux + faststart (works for your H.264/AAC MP4s, ~no CPU)
    rc, err = await _run('ffmpeg', '-y', '-i', str(raw), '-c', 'copy',
                         '-movflags', '+faststart', str(out))
    if rc != 0 or not out.exists():
        # 2) fallback full re-encode at low priority (HEVC/odd codecs); won't starve bots
        out.unlink(missing_ok=True)
        rc, err = await _run('nice', '-n', '15', 'ffmpeg', '-y', '-i', str(raw),
                             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
                             '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(out))
    raw.unlink(missing_ok=True)
    vtt = None
    if sub_raw and sub_raw.exists():
        vtt_path = MEDIA / f'{mid}.vtt'
        rc2, _ = await _run('ffmpeg', '-y', '-i', str(sub_raw), str(vtt_path))
        sub_raw.unlink(missing_ok=True)
        if vtt_path.exists():
            vtt = f'{mid}.vtt'
    r = load_reg()
    if mid in r:
        r[mid]['status'] = 'ready' if out.exists() else 'error'
        r[mid]['vtt'] = vtt
        if out.exists():
            r[mid]['error'] = ''
        else:
            r[mid]['error'] = err
        save_reg(r)

@app.post('/api/delete')
def api_delete(key: str = Form(...), id: str = Form(...)):
    check_key(key)
    r = load_reg()
    if id in r:
        for ext in ('mp4', 'vtt', 'srt', 'raw'):
            (MEDIA / f'{id}.{ext}').unlink(missing_ok=True)
        del r[id]
        save_reg(r)
    return {'ok': True}

@app.get('/w/{room}', response_class=HTMLResponse)
def watch(room: str):
    r = load_reg()
    mv = next((v for v in r.values() if v['room'] == room), None)
    if not mv:
        raise HTTPException(404, 'room not found')
    html = (STATIC / 'player.html').read_text(encoding='utf-8')
    return (html
            .replace('__VIDEO__', f'/media/{mv["file"]}')
            .replace('__VTT__', f'/media/{mv["vtt"]}' if mv.get('vtt') else '')
            .replace('__TITLE__', mv['title'].replace('<', '').replace('>', ''))
            .replace('__ROOM__', room)
            .replace('__STATUS__', mv['status']))

@app.websocket('/ws/{room}')
async def ws(websocket: WebSocket, room: str):
    await websocket.accept()
    rm = rooms.setdefault(room, {'state': None, 'clients': set()})
    rm['clients'].add(websocket)
    await _broadcast_presence(rm)
    if rm['state'] is not None:
        await websocket.send_text(json.dumps({'type': 'state', **rm['state']}))
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
            except Exception:
                continue
            if msg.get('type') == 'state':
                rm['state'] = {'paused': bool(msg.get('paused', True)), 'time': float(msg.get('time', 0))}
            dead = []
            for c in list(rm['clients']):
                if c is not websocket:
                    try:
                        await c.send_text(data)
                    except Exception:
                        dead.append(c)
            for d in dead:
                rm['clients'].discard(d)
    except WebSocketDisconnect:
        pass
    finally:
        rm['clients'].discard(websocket)
        await _broadcast_presence(rm)

async def _broadcast_presence(rm):
    n = len(rm['clients'])
    msg = json.dumps({'type': 'presence', 'count': n})
    for c in list(rm['clients']):
        try:
            await c.send_text(msg)
        except Exception:
            pass
