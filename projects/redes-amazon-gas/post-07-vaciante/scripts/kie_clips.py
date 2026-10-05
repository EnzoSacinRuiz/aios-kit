"""Post 7 (vaciante): anima fotos reales de Amazon Gas con kie.ai (Kling 2.1 Standard, image-to-video).

Mismo patrón que post-01-rio/scripts/kie_clips.py, con otras fotos y otros encuadres para que
no se sienta repetido. Reintenta con backoff si kie.ai responde 429 (otros agentes usan la API).
"""
import base64, io, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[2]
FOTOS = AIOS / "references/branding/fotos"
OUT = ROOT / "assets/clips"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["KIE_AI_API_KEY"].strip().strip('"')
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
NEG = "blur, distortion, warped text, deformed logo, extra objects, extra boats, people morphing, low quality"

# (id, foto, centro horizontal del recorte 0..1, prompt)
SHOTS = [
    ("v1-rio", "rio", 0.50,
     "A river barge carrying white gas tanks, pushed by a small tugboat, sails slowly to the right across a calm wide "
     "brown Amazon river at sunrise, gentle ripples and reflections on the water, realistic documentary footage, "
     "stable camera, keep the boat and tanks unchanged, no new objects"),
    ("v2-meandro", "aerea-meandro", 0.80,
     "Aerial drone shot slowly pulling back and rising over the Amazon rainforest, the winding river channel curves "
     "through the jungle, light haze, realistic, stable camera, keep everything unchanged, no new objects"),
    ("v3-barcaza", "barcaza-real", 0.60,
     "A moored river barge on the Amazon riverbank, slow cinematic push-in toward the deck, calm water ripples, "
     "leaves move lightly in the breeze, the worker stands still, realistic documentary footage, "
     "keep all equipment, signs and people unchanged"),
]


def req(url, data=None, headers=H, tries=5):
    wait = 30
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
            d = json.loads(urllib.request.urlopen(r, timeout=120).read())
            if isinstance(d, dict) and d.get("code") == 429:
                raise urllib.error.HTTPError(url, 429, "rate", None, None)
            return d
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                print("429, espero", wait, flush=True)
                time.sleep(wait)
                wait = min(wait * 2, 120)
                continue
            raise


def credits():
    try:
        return req("https://api.kie.ai/api/v1/chat/credit").get("data")
    except Exception as e:  # noqa: BLE001
        return f"err {e}"


def crop_916(name, cx, sid):
    im = Image.open(FOTOS / f"{name}.webp").convert("RGB")
    w, h = im.size
    cw = int(h * 9 / 16)
    left = max(0, min(w - cw, int(cx * w - cw / 2)))
    im = im.crop((left, 0, left + cw, h)).resize((720, 1280), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    (OUT / f"{sid}-916.jpg").write_bytes(buf.getvalue())
    return base64.b64encode(buf.getvalue()).decode()


def main():
    only = set(sys.argv[1:])
    log = {"credits_before": credits(), "tasks": {}}
    tasks = {}
    for sid, foto, cx, prompt in SHOTS:
        if only and sid not in only:
            continue
        b64 = crop_916(foto, cx, sid)
        up = req("https://kieai.redpandaai.co/api/file-base64-upload",
                 {"base64Data": f"data:image/jpeg;base64,{b64}", "uploadPath": "amazongas", "fileName": f"p07-{sid}.jpg"})
        url = up["data"].get("downloadUrl") or up["data"]["fileUrl"]
        t = req("https://api.kie.ai/api/v1/jobs/createTask", {
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
            try:
                d = req(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
            except Exception as e:  # noqa: BLE001
                print("poll err", sid, e, flush=True)
                continue
            if d["state"] == "success":
                u = json.loads(d["resultJson"])["resultUrls"][0]
                urllib.request.urlretrieve(u, OUT / f"{sid}.mp4")
                log["tasks"][sid] = {"taskId": tid, "credits": d.get("creditsConsumed"), "url": u}
                print(sid, "OK credits", d.get("creditsConsumed"), flush=True)
                pending.pop(sid)
            elif d["state"] == "fail":
                log["tasks"][sid] = {"taskId": tid, "fail": d.get("failMsg")}
                print(sid, "FAIL", d.get("failMsg"), flush=True)
                pending.pop(sid)
    log["credits_after"] = credits()
    log["pending_timeout"] = list(pending)
    prev = OUT / "credits.json"
    hist = json.loads(prev.read_text()) if prev.exists() else []
    hist = hist if isinstance(hist, list) else [hist]
    hist.append(log)
    prev.write_text(json.dumps(hist, indent=2, ensure_ascii=False))
    print(json.dumps({k: log[k] for k in ("credits_before", "credits_after", "pending_timeout")}))


if __name__ == "__main__":
    main()
