"""Post 3 (tacacho con cecina): genera escenas de cocina con kie.ai.

1. Imagen 9:16 con Nano Banana (google/nano-banana) por escena.
2. Las escenas con movimiento se animan con Kling 2.1 Standard (image-to-video, 5 s).
El fondo de cocina para el plano del balón queda como imagen fija: el balón se compone
encima en HTML desde la foto real (references/branding/fotos/balon-15kg.webp).

Registra créditos en assets/clips/credits.json. Reintenta con backoff si hay 429.
Uso: python3 scripts/kie_clips.py [id ...]
"""
import json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/clips"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["KIE_AI_API_KEY"].strip().strip('"')
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

STYLE = ("photorealistic food documentary photography, rustic home kitchen in Iquitos, Peruvian Amazon, "
         "warm natural morning light, shallow depth of field, vertical 9:16 composition, "
         "no text, no logos, no gas cylinders, no tanks, no faces")
NEG = "blur, distortion, warped hands, extra fingers, text, logo, gas cylinder, faces, morphing food, low quality"

# (id, prompt de imagen, prompt de movimiento o None si es fija)
SHOTS = [
    ("s1-platano",
     "Close-up of hands peeling green plantains (platano bellaco) on a worn wooden cutting board, chunks of green "
     "plantain beside a knife, banana leaves in the background. " + STYLE,
     "Hands slowly peel the green plantain, subtle natural movement, gentle slow camera push-in, realistic"),
    ("s2-fritura",
     "Close-up of thick chunks of green plantain frying golden in a black iron pan, the pan sits on a home stove "
     "burner with a steady even ring of blue gas flame clearly visible under the pan, oil gently bubbling. " + STYLE,
     "Oil bubbles gently around the plantain chunks, the blue flame flickers steadily under the pan, slow push-in, realistic"),
    ("s3-machacar",
     "Hands mashing golden fried plantain together with crispy pork chicharron and a spoon of lard in a wooden "
     "bowl with a wooden pestle, overhead three-quarter angle. " + STYLE,
     "The hands press and mash the fried plantain with the wooden pestle, slow steady motion, realistic"),
    ("s4-bolitas",
     "Close-up of hands shaping a round golden ball of tacacho (mashed fried green plantain with pork cracklings), "
     "two finished tacacho balls on a banana leaf next to them. " + STYLE,
     "The hands slowly roll and shape the tacacho ball, gentle motion, slow camera push-in, realistic"),
    ("s5-cecina",
     "Close-up of strips of reddish smoked pork cecina sizzling in a cast iron pan, the pan sits on a home stove "
     "burner with an even ring of blue gas flame visible beneath, light smoke rising. " + STYLE,
     "The cecina sizzles, light smoke rises, the blue flame burns steadily, slow camera push-in, realistic"),
    ("s6-plato",
     "Breakfast plate of tacacho con cecina: two golden tacacho balls and fried reddish smoked pork cecina served "
     "on a banana leaf over a rustic wooden table, a cup of black coffee and a slice of lime beside it, "
     "three-quarter angle. " + STYLE,
     "Steam rises gently from the food, slow cinematic orbit around the plate, realistic, food stays unchanged"),
    ("bg-cocina",
     "Rustic Amazonian home kitchen interior in Iquitos: on the right a simple two-burner stove on a tiled counter "
     "with an iron pan on it, the lower-left area of the frame is an empty clean tiled floor and wall corner in "
     "the foreground, window with green jungle light. " + STYLE,
     None),
]


def req(url, data=None, tries=5):
    wait = 30
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=H)
            d = json.loads(urllib.request.urlopen(r, timeout=120).read())
            if d.get("code") == 429:
                raise urllib.error.HTTPError(url, 429, "rate", None, None)
            return d
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


def create(model, inp):
    t = req("https://api.kie.ai/api/v1/jobs/createTask", {"model": model, "input": inp})
    if not t.get("data"):
        raise RuntimeError(f"createTask {model}: {t}")
    return t["data"]["taskId"]


def wait_all(tasks, timeout=1800):
    done, pending = {}, dict(tasks)
    deadline = time.time() + timeout
    while pending and time.time() < deadline:
        time.sleep(15)
        for sid, tid in list(pending.items()):
            d = req(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
            if d["state"] == "success":
                done[sid] = {"taskId": tid, "url": json.loads(d["resultJson"])["resultUrls"][0],
                             "credits": d.get("creditsConsumed")}
                print(sid, "OK", d.get("creditsConsumed"), flush=True)
                pending.pop(sid)
            elif d["state"] == "fail":
                done[sid] = {"taskId": tid, "fail": d.get("failMsg")}
                print(sid, "FAIL", d.get("failMsg"), flush=True)
                pending.pop(sid)
    return done, list(pending)


def main():
    only = set(sys.argv[1:])
    shots = [s for s in SHOTS if not only or s[0] in only]
    logf = OUT / "credits.json"
    log = json.loads(logf.read_text()) if logf.exists() else {"runs": []}
    run = {"credits_before": credits(), "images": {}, "videos": {}}

    img_tasks = {sid: create("google/nano-banana", {"prompt": p, "output_format": "png", "image_size": "9:16"})
                 for sid, p, _ in shots}
    imgs, pend = wait_all(img_tasks, 900)
    run["images"] = imgs
    for sid, r in imgs.items():
        if "url" in r:
            urllib.request.urlretrieve(r["url"], OUT / f"{sid}.png")

    vid_tasks = {}
    for sid, _, motion in shots:
        if motion and "url" in imgs.get(sid, {}):
            vid_tasks[sid] = create("kling/v2-1-standard", {
                "prompt": motion, "image_url": imgs[sid]["url"], "duration": "5",
                "negative_prompt": NEG, "cfg_scale": 0.5})
            print(sid, "video task", vid_tasks[sid], flush=True)
    vids, pend2 = wait_all(vid_tasks)
    run["videos"] = vids
    for sid, r in vids.items():
        if "url" in r:
            urllib.request.urlretrieve(r["url"], OUT / f"{sid}.mp4")
    run["credits_after"] = credits()
    run["pending_timeout"] = pend + pend2
    log["runs"].append(run)
    logf.write_text(json.dumps(log, indent=2, ensure_ascii=False))
    print(json.dumps({k: run[k] for k in ("credits_before", "credits_after", "pending_timeout")}))


if __name__ == "__main__":
    main()
