"""Post 6 · Señor de los Milagros — genera los recursos con IA.

1. kie.ai (Seedream v4, texto→imagen): fondo de velas encendidas y flores blancas, sin imágenes
   sagradas ni personas. -> assets/fondo.png
2. kie.ai (Kling 2.1 Standard, imagen→video 5 s): leve parpadeo de las llamas. -> assets/velas.mp4
3. ElevenLabs Music: música solemne suave, instrumental, 12 s. -> assets/musica.mp3

Registra créditos en assets/creditos.json. Uso: python3 scripts/generar.py [imagen] [video] [musica]
Reintenta con backoff si hay 429 (otros agentes usan las mismas APIs).
"""
import base64, io, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[2]
A = ROOT / "assets"
A.mkdir(exist_ok=True)
env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KIE = env["KIE_AI_API_KEY"].strip().strip('"')
XI = env["ELEVENLABS_API_KEY"].strip().strip('"')
H = {"Authorization": f"Bearer {KIE}", "Content-Type": "application/json"}
LOG = A / "creditos.json"
log = json.loads(LOG.read_text()) if LOG.exists() else {}

PROMPT_IMG = (
    "Photorealistic close-up of many small lit white candles in glass votive holders arranged on a dark wooden "
    "surface at night, surrounded by fresh white lilies and white roses, warm golden candlelight, soft amber bokeh "
    "in the dark background, reverent, calm and solemn atmosphere, shallow depth of field, cinematic, vertical "
    "composition with the candles and flowers in the lower half and dark empty warm space in the upper half. "
    "Color palette: warm amber, cream, deep brown, touches of dark maroon. Absolutely no purple or violet anywhere, "
    "no people, no faces, no religious statues or paintings, no crosses, no text, no logos."
)
PROMPT_VID = (
    "Static camera. The candle flames flicker gently and softly, warm light breathes slightly, very subtle movement, "
    "everything else stays perfectly still, realistic, calm, solemn"
)
NEG = "camera shake, zoom, new objects, people, faces, text, purple, violet, distortion, morphing, low quality"
PROMPT_MUS = (
    "Solemn, reverent and gentle instrumental for a quiet moment of faith. Soft sustained strings and a slow, "
    "tender piano melody, warm and hopeful, no drums, no percussion, no vocals. Slow tempo, calm, ends softly."
)


def call(url, data=None, headers=H, raw=False, timeout=180):
    for espera in (0, 30, 60, 120, 120):
        if espera:
            print(f"  429/err, espero {espera}s", flush=True)
            time.sleep(espera)
        try:
            r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
            body = urllib.request.urlopen(r, timeout=timeout).read()
            if raw:
                return body
            d = json.loads(body)
            if isinstance(d, dict) and d.get("code") in (429, 455, 500, 503):
                print("  kie code", d.get("code"), d.get("msg"), flush=True)
                continue
            return d
        except urllib.error.HTTPError as e:
            msg = e.read()[:300]
            if e.code in (429, 500, 502, 503):
                print("  http", e.code, msg, flush=True)
                continue
            raise SystemExit(f"HTTP {e.code}: {msg}")
    raise SystemExit("demasiados reintentos")


def kie_credits():
    try:
        return call("https://api.kie.ai/api/v1/chat/credit").get("data")
    except SystemExit as e:
        return str(e)


def kie_task(model, inp, timeout=1500):
    t = call("https://api.kie.ai/api/v1/jobs/createTask", {"model": model, "input": inp})
    if not t.get("data"):
        raise SystemExit(f"createTask falló: {t}")
    tid = t["data"]["taskId"]
    print(model, "task", tid, flush=True)
    fin = time.time() + timeout
    while time.time() < fin:
        time.sleep(15)
        d = call(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
        if d["state"] == "success":
            return tid, json.loads(d["resultJson"])["resultUrls"][0], d.get("creditsConsumed")
        if d["state"] == "fail":
            raise SystemExit(f"fail: {d.get('failMsg')}")
    raise SystemExit("timeout")


def imagen():
    antes = kie_credits()
    tid, url, cred = kie_task("bytedance/seedream-v4-text-to-image",
                              {"prompt": PROMPT_IMG, "image_size": "portrait_16_9", "image_resolution": "2K", "max_images": 1})
    urllib.request.urlretrieve(url, A / "fondo.png")
    log["imagen"] = {"model": "seedream-v4", "taskId": tid, "creditsConsumed": cred, "kie_antes": antes, "kie_despues": kie_credits()}


def video():
    from PIL import Image
    im = Image.open(A / "fondo.png").convert("RGB")
    im = im.resize((720, int(720 * im.height / im.width)))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    up = call("https://kieai.redpandaai.co/api/file-base64-upload",
              {"base64Data": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
               "uploadPath": "amazongas", "fileName": "post06-velas.jpg"})
    src = up["data"].get("downloadUrl") or up["data"]["fileUrl"]
    antes = kie_credits()
    tid, url, cred = kie_task("kling/v2-1-standard",
                              {"prompt": PROMPT_VID, "image_url": src, "duration": "5", "negative_prompt": NEG, "cfg_scale": 0.5})
    urllib.request.urlretrieve(url, A / "velas.mp4")
    log["video"] = {"model": "kling-2.1-standard 5s", "taskId": tid, "creditsConsumed": cred, "kie_antes": antes, "kie_despues": kie_credits()}


def musica():
    audio = call("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                 {"prompt": PROMPT_MUS, "music_length_ms": 13000},
                 headers={"xi-api-key": XI, "Content-Type": "application/json"}, raw=True, timeout=300)
    (A / "musica.mp3").write_bytes(audio)
    log["musica"] = {"api": "elevenlabs music", "length_ms": 13000, "bytes": len(audio)}


if __name__ == "__main__":
    pasos = sys.argv[1:] or ["imagen", "video", "musica"]
    for p in pasos:
        globals()[p]()
        LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
        print(p, "OK", flush=True)
    print(json.dumps(log, indent=2))
