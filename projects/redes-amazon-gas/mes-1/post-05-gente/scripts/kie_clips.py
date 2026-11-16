"""Anima fotos reales del post 5 (simulacro y capacitación) con kie.ai (Kling 2.1 Standard, image-to-video).

Mismo patrón que post-01-rio/scripts/kie_clips.py. Cada toma se envía recortada a 9:16 o
entera (16:9, para panear luego en HyperFrames). Reintenta con backoff si hay 429.
Registra los créditos en assets/clips/credits.json.

Uso: python3 scripts/kie_clips.py [id ...]   (sin ids: todas)
"""
import base64, io, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
FOTOS = AIOS / "references/branding/fotos"
OUT = ROOT / "assets/clips"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["KIE_AI_API_KEY"].strip().strip('"')
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
NEG = ("blur, distortion, face morphing, deformed faces, extra people, extra limbs, warped text, "
       "deformed logo, new objects, fire, flames, low quality")

# (id, foto, recorte: "full" o centro horizontal 0..1 para 9:16, prompt)
SHOTS = [
    ("s1-simulacro", "simulacro", "full",
     "Real documentary footage of a fire drill: a worker in a white helmet sprays a red fire extinguisher, "
     "white powder cloud billows and drifts slowly around the red barrel, the watching workers stand still, "
     "very subtle handheld camera, realistic, keep every person's face and body unchanged"),
    ("s2-capacitacion", "capacitacion", 0.47,
     "Real documentary footage: two workers in blue helmets hold a fire hose and spray a strong water jet into the air "
     "next to river barges, water spray falls and drifts, slight slow camera push-in, realistic, "
     "keep the workers, cones, barges and tanks unchanged"),
]


def req(url, data=None, headers=H, tries=4):
    wait = 30
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
            return json.loads(urllib.request.urlopen(r, timeout=120).read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                print("429, espero", wait, flush=True)
                time.sleep(wait)
                wait *= 2
                continue
            raise


def credits():
    try:
        return req("https://api.kie.ai/api/v1/chat/credit").get("data")
    except Exception as e:  # noqa: BLE001
        return f"err {e}"


def prep(name, crop):
    im = Image.open(FOTOS / f"{name}.webp").convert("RGB")
    w, h = im.size
    if crop == "full":
        im = im.resize((1280, 720), Image.LANCZOS)
        tag = "169"
    else:
        cw = int(h * 9 / 16)
        left = max(0, min(w - cw, int(crop * w - cw / 2)))
        im = im.crop((left, 0, left + cw, h)).resize((720, 1280), Image.LANCZOS)
        tag = "916"
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    (OUT / f"{name}-{tag}.jpg").write_bytes(buf.getvalue())
    return base64.b64encode(buf.getvalue()).decode()


def main():
    only = set(sys.argv[1:])
    log = {"credits_before": credits(), "tasks": {}}
    tasks = {}
    for sid, foto, crop, prompt in SHOTS:
        if only and sid not in only:
            continue
        b64 = prep(foto, crop)
        up = req("https://kieai.redpandaai.co/api/file-base64-upload",
                 {"base64Data": f"data:image/jpeg;base64,{b64}", "uploadPath": "amazongas", "fileName": f"p5-{sid}.jpg"})
        url = up["data"].get("downloadUrl") or up["data"]["fileUrl"]
        t = req("https://api.kie.ai/api/v1/jobs/createTask", {
            "model": "kling/v2-1-standard",
            "input": {"prompt": prompt, "image_url": url, "duration": "5", "negative_prompt": NEG, "cfg_scale": 0.5},
        })
        tasks[sid] = t["data"]["taskId"]
        print(sid, "task", tasks[sid], flush=True)

    pending = dict(tasks)
    deadline = time.time() + 1800
    while pending and time.time() < deadline:
        time.sleep(20)
        for sid, tid in list(pending.items()):
            d = req(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
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
