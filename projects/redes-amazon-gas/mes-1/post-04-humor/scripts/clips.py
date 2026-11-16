"""Planos animados del post 4 con kie.ai.

- Planos con diálogo (a, b, c): Kling AI Avatar Standard = imagen de escena + audio de ElevenLabs,
  con sincronía labial.
- Inserto (d): Kling 2.1 Standard imagen→video, la llama de la hornilla se apaga.

Uso: python3 clips.py [a b c d]
"""
import json, sys
import kie

ROOT = kie.ROOT
IMG = ROOT / "assets/img"
AUD = ROOT / "assets/audio"
OUT = ROOT / "assets/clips"
OUT.mkdir(exist_ok=True)
LOG = OUT / "credits.json"

AVATAR = {
    "a": ("a-cocinando", "The woman talks happily to the camera while stirring the pot, proud and cheerful, natural "
                         "head movement, steam rising, realistic."),
    "b": ("b-susto", "The woman talks to the camera in comedic disbelief, shocked and dramatic, hands move from her "
                     "cheeks as she speaks, expressive eyebrows, realistic."),
    "c": ("c-celular", "The woman gives friendly wise advice to the camera, raising her index finger, then shows "
                       "the phone, warm knowing smile, realistic."),
}
INSERT_PROMPT = ("Static close-up: the small blue gas flame under the pot flickers weakly, sputters and goes out "
                 "completely, the steam fades away. Camera does not move. Realistic, nothing else changes.")


def img_url_for(name):
    """Usa la URL pública que devolvió nano-banana-2; si no, sube un JPEG 1080x1920 liviano."""
    gen = json.loads((IMG / "credits.json").read_text()).get(name, {})
    if gen.get("urls"):
        return gen["urls"][0]
    from PIL import Image
    jpg = OUT / f"{name}.jpg"
    Image.open(IMG / f"{name}.png").convert("RGB").resize((1080, 1920)).save(jpg, quality=90)
    return kie.upload(jpg, "image/jpeg")


def main():
    only = set(sys.argv[1:]) or {"a", "b", "c", "d"}
    log = json.loads(LOG.read_text()) if LOG.exists() else {}
    tasks = {}
    for k, (img, prompt) in AVATAR.items():
        if k not in only:
            continue
        img_url = img_url_for(img)
        aud_url = kie.upload(AUD / f"voz-{k}.mp3", "audio/mpeg")
        tasks[k] = kie.create("kling/ai-avatar-standard", {"image_url": img_url, "audio_url": aud_url, "prompt": prompt})
        print(k, tasks[k], flush=True)
    if "d" in only:
        img_url = img_url_for("d-hornilla")
        tasks["d"] = kie.create("kling/v2-1-standard", {
            "prompt": INSERT_PROMPT, "image_url": img_url, "duration": "5",
            "negative_prompt": "camera movement, new objects, people, text, purple", "cfg_scale": 0.5})
        print("d", tasks["d"], flush=True)
    res = kie.wait_all(tasks, timeout=2400, every=20)
    for k, r in res.items():
        if r["state"] == "success":
            kie.download(r["urls"][0], OUT / f"{k}.mp4")
        log[k] = r
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
    print(json.dumps(res))


if __name__ == "__main__":
    main()
