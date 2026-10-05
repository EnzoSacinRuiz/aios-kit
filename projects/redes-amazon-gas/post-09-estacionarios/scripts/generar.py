"""Post 9 — tanques estacionarios. Genera los insumos del video.

Pasos (python3 scripts/generar.py [clips] [voz] [musica]; sin argumentos: todos):
- clips: anima 4 fotos reales con kie.ai (Kling 2.1 Standard, imagen→video, 5 s).
- voz: voz en off con Terry (ElevenLabs) + alineación por carácter.
- musica: cama musical corta (ElevenLabs music).
Registra créditos y caracteres en assets/log.json. Reintenta con backoff ante 429.
"""
import base64, io, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[2]
FOTOS = AIOS / "references/branding/fotos"
CLIPS = ROOT / "assets/clips"
AUDIO = ROOT / "assets/audio"
LOG = ROOT / "assets/log.json"
for d in (CLIPS, AUDIO):
    d.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KIE = env["KIE_AI_API_KEY"].strip().strip('"')
XI = env["ELEVENLABS_API_KEY"].strip().strip('"')
HK = {"Authorization": f"Bearer {KIE}", "Content-Type": "application/json"}
NEG = "blur, distortion, warped text, deformed logo, changing letters, extra objects, people appearing, morphing, low quality"
VOICE = "ulJB4yAMefhHYn0FWgGy"  # Terry

log = json.loads(LOG.read_text()) if LOG.exists() else {}

# (id, foto, centro x 0..1, recorte inferior en px para quitar marcas, prompt)
SHOTS = [
    ("s1-bateria", "bateria-45", 0.52, 40,
     "Slow cinematic push-in on a row of brown gas cylinders connected to a wall manifold in a commercial kitchen "
     "service area, realistic, static objects, keep all labels, letters and logos exactly unchanged"),
    ("s2-tanques", "estacionarios-1", 0.45, 0,
     "Slow smooth dolly forward along white stationary LPG tanks with the Amazon Gas logo, soft daylight, "
     "realistic, tanks stay perfectly still, keep the logo and lettering exactly unchanged"),
    ("s3-azotea", "estacionarios-2", 0.33, 0,
     "Slow lateral camera move on a rooftop with white stationary gas tanks, clouds drift slowly in the sky, "
     "palm leaves sway lightly, realistic, keep tanks, logos and lettering exactly unchanged"),
    ("s4-cisterna", "cisterna-real", 0.62, 0,
     "Slow gentle camera push-in toward a parked LPG tanker truck with the Amazon Gas logo, clouds move in the sky, "
     "grass moves slightly in the breeze, realistic, keep the truck, logo and lettering exactly unchanged"),
]


def call(url, data=None, headers=HK, raw=False, timeout=120):
    for espera in (0, 30, 60, 120, 120):
        if espera:
            print(f"  429/err, espero {espera}s", flush=True)
            time.sleep(espera)
        try:
            r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
            body = urllib.request.urlopen(r, timeout=timeout).read()
            if raw:
                return body
            j = json.loads(body)
            if isinstance(j, dict) and j.get("code") == 429:
                continue
            return j
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read()[:300]!r}")
    raise RuntimeError("demasiados reintentos")


def kie_credits():
    try:
        return call("https://api.kie.ai/api/v1/chat/credit").get("data")
    except Exception as e:  # noqa: BLE001
        return f"err {e}"


def crop_916(name, cx, cut_bottom):
    im = Image.open(FOTOS / f"{name}.webp").convert("RGB")
    w, h = im.size
    h -= cut_bottom
    cw = int(h * 9 / 16)
    left = max(0, min(w - cw, int(cx * w - cw / 2)))
    im = im.crop((left, 0, left + cw, h)).resize((720, 1280), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    (CLIPS / f"{name}-916.jpg").write_bytes(buf.getvalue())
    return base64.b64encode(buf.getvalue()).decode()


def clips():
    only = set(a for a in sys.argv[2:])
    log.setdefault("kie", {})["credits_before"] = kie_credits()
    tasks = {}
    for sid, foto, cx, cut, prompt in SHOTS:
        if only and sid not in only:
            continue
        b64 = crop_916(foto, cx, cut)
        up = call("https://kieai.redpandaai.co/api/file-base64-upload",
                  {"base64Data": f"data:image/jpeg;base64,{b64}", "uploadPath": "amazongas", "fileName": f"p09-{sid}.jpg"})
        url = up["data"].get("downloadUrl") or up["data"]["fileUrl"]
        t = call("https://api.kie.ai/api/v1/jobs/createTask", {
            "model": "kling/v2-1-standard",
            "input": {"prompt": prompt, "image_url": url, "duration": "5", "negative_prompt": NEG, "cfg_scale": 0.5},
        })
        tasks[sid] = t["data"]["taskId"]
        print(sid, "task", tasks[sid], flush=True)
    pending = dict(tasks)
    deadline = time.time() + 2400
    while pending and time.time() < deadline:
        time.sleep(20)
        for sid, tid in list(pending.items()):
            d = call(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
            if d["state"] == "success":
                u = json.loads(d["resultJson"])["resultUrls"][0]
                urllib.request.urlretrieve(u, CLIPS / f"{sid}.mp4")
                log["kie"].setdefault("tasks", {})[sid] = {"taskId": tid, "credits": d.get("creditsConsumed")}
                print(sid, "OK", d.get("creditsConsumed"), flush=True)
                pending.pop(sid)
            elif d["state"] == "fail":
                log["kie"].setdefault("tasks", {})[sid] = {"taskId": tid, "fail": d.get("failMsg")}
                print(sid, "FAIL", d.get("failMsg"), flush=True)
                pending.pop(sid)
    log["kie"]["credits_after"] = kie_credits()
    log["kie"]["pending_timeout"] = list(pending)


TEXTO = (
    "¿Tienes restaurante o panadería? "
    "Entonces ya no vuelvas a cambiar balones. "
    "Con un tanque estacionario de Amazon Gas, desde ochenta galones, tu negocio tiene gas de corrido. "
    "Nosotros lo instalamos, y nuestra cisterna lo llena ahí mismo, en tu local. "
    "Cotiza por WhatsApp."
)


def voz():
    body = {"text": TEXTO, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}}
    d = call(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
             body, headers={"xi-api-key": XI, "Content-Type": "application/json"}, timeout=180)
    (AUDIO / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (AUDIO / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
    log["voz"] = {"api": "elevenlabs tts eleven_multilingual_v2", "voice": "Terry", "chars": len(TEXTO),
                  "dur": d["alignment"]["character_end_times_seconds"][-1]}


PROMPT_MUS = ("Warm, upbeat Peruvian Amazon cumbia instrumental for a small-business commercial, light guitar riff, "
              "soft percussion, positive and confident, steady groove, no vocals, clean ending")


def musica():
    audio = call("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                 {"prompt": PROMPT_MUS, "music_length_ms": 22000},
                 headers={"xi-api-key": XI, "Content-Type": "application/json"}, raw=True, timeout=300)
    (AUDIO / "musica.mp3").write_bytes(audio)
    log["musica"] = {"api": "elevenlabs music", "length_ms": 22000, "bytes": len(audio)}


if __name__ == "__main__":
    pasos = sys.argv[1:2] or ["clips", "voz", "musica"]
    if pasos == ["todo"]:
        pasos = ["clips", "voz", "musica"]
    for p in pasos:
        globals()[p]()
        LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
        print(p, "OK", flush=True)
