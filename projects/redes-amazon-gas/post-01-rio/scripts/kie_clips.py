"""Anima fotos reales de Amazon Gas con kie.ai (Kling 2.1 Standard, image-to-video).

Recorta cada foto a 9:16, la sube a kie.ai, crea la tarea, espera el resultado y
descarga el mp4 en assets/clips/. Registra los créditos consumidos en
assets/clips/credits.json.
"""
import base64, io, json, re, sys, time, urllib.request
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
NEG = "blur, distortion, warped text, deformed logo, extra objects, people morphing, low quality"

# (id, foto, centro horizontal del recorte 0..1, prompt)
SHOTS = [
    ("s1-meandro", "aerea-meandro", 0.22,
     "Aerial drone shot slowly gliding forward over the Amazon rainforest, the wide brown river gently flowing, "
     "soft morning haze, realistic, stable camera, no new objects"),
    ("s2-barcaza", "barcaza", 0.42,
     "A moored river barge on the Amazon, calm water ripples gently, clouds drift slowly, subtle slow camera pan "
     "to the right, realistic documentary footage, keep all equipment and signs unchanged"),
    ("s3-planta", "aerea-planta", 0.50,
     "Aerial drone shot slowly descending toward an industrial plant surrounded by jungle next to the river, "
     "trees sway lightly, realistic, stable, keep buildings unchanged"),
    ("s4-balones", "balones-stock", 0.40,
     "Slow cinematic dolly push-in over rows of gas cylinders in a warehouse yard, soft daylight, realistic, "
     "cylinders stay perfectly still and unchanged"),
    ("s5-camion", "camion-balones", 0.62,
     "A delivery truck loaded with gas cylinders parked on a road in the Amazon, slow gentle camera push-in, "
     "leaves move in the breeze, realistic, keep the truck sign and logo unchanged"),
]


def req(url, data=None, headers=H):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=headers)
    return json.loads(urllib.request.urlopen(r, timeout=120).read())


def credits():
    try:
        return req("https://api.kie.ai/api/v1/chat/credit").get("data")
    except Exception as e:  # noqa: BLE001
        return f"err {e}"


def crop_916(name, cx):
    im = Image.open(FOTOS / f"{name}.webp").convert("RGB")
    w, h = im.size
    cw = int(h * 9 / 16)
    left = max(0, min(w - cw, int(cx * w - cw / 2)))
    im = im.crop((left, 0, left + cw, h)).resize((720, 1280), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=92)
    (OUT / f"{name}-916.jpg").write_bytes(buf.getvalue())
    return base64.b64encode(buf.getvalue()).decode()


def main():
    only = set(sys.argv[1:])
    log = {"credits_before": credits(), "tasks": {}}
    tasks = {}
    for sid, foto, cx, prompt in SHOTS:
        if only and sid not in only:
            continue
        b64 = crop_916(foto, cx)
        up = req("https://kieai.redpandaai.co/api/file-base64-upload",
                 {"base64Data": f"data:image/jpeg;base64,{b64}", "uploadPath": "amazongas", "fileName": f"{sid}.jpg"})
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
    (OUT / "credits.json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
    print(json.dumps({k: log[k] for k in ("credits_before", "credits_after", "pending_timeout")}))


if __name__ == "__main__":
    main()
