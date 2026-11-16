"""Mes 2, post 1 (precinto): imágenes y clips con kie.ai.

⚠️ TEMPORALES: el primer plano del precinto (b-precinto) es IA y NO lleva el texto real. Se reemplaza
por la grabación real del precinto antes de publicar. El texto "Amazon Gas" del precinto no se genera
(la IA lo deforma); va como gráfico en HyperFrames.

- img: Nano Banana 2 con las fotos reales del balón de 10 kg y del stock como referencia.
- vid: Kling 2.1 Standard anima esas imágenes.

Uso: python3 scripts/clips.py img | vid [ids...]
"""
import json, sys
from PIL import Image
import kie

ROOT = kie.ROOT
FOTOS = kie.AIOS / "references/branding/fotos"
OUT = ROOT / "assets/clips"
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "credits.json"

ESTILO = ("Photorealistic documentary photo, vertical 9:16, natural warm daylight, Iquitos in the Peruvian Amazon, "
          "shallow depth of field. The gas cylinder is exactly the brown 10 kg AMAZON GAS cylinder from the "
          "reference: brown body, yellow triangle logo with flame, white 'AMAZON GAS' text. No other brands. "
          "The yellow plastic seal on the valve is plain, with no text on it.")
IMAGENES = {
    "a-entrega": "At the wooden front door of a simple colorful house in Iquitos, a delivery man in a dark uniform "
                 "hands a brown AMAZON GAS 10 kg cylinder to a smiling local woman in her forties, the cylinder is "
                 "the center of the frame, tropical plants around, medium shot.",
    "b-precinto": "Extreme close-up from above of the valve of a brown AMAZON GAS cylinder sealed with an intact "
                  "bright yellow plastic security seal cap, the seal fills the center of the frame, the yellow "
                  "logo on the cylinder shoulder is visible below, soft background.",
    "c-revisa": "In a simple Loreto home kitchen, a woman's hands hold and inspect the yellow plastic security seal "
                "on top of a brown AMAZON GAS cylinder, close-up over the shoulder, a gas stove blurred behind.",
}
VIDEOS = {  # id: prompt
    "a-entrega": "The delivery man hands the gas cylinder to the woman, she takes it and nods, slow gentle "
                 "push-in, realistic, keep the logo and cylinder unchanged.",
    "b-precinto": "Very slow cinematic push-in toward the yellow seal on the valve, light shifts softly, "
                  "realistic, keep the seal and logo unchanged.",
    "c-revisa": "The woman's fingers turn the cylinder slightly and touch the yellow seal to check it is intact, "
                "slow and steady, realistic, keep the logo unchanged.",
}
NEG = "blur, distortion, warped text, deformed logo, extra objects, morphing, text on the seal, low quality"


def jpg(path, size=None):
    im = Image.open(path).convert("RGB")
    if size:
        im.thumbnail(size)
    dest = OUT / f"ref-{path.stem}.jpg"
    im.save(dest, "JPEG", quality=92)
    return dest


def load():
    return json.loads(LOG.read_text()) if LOG.exists() else {}


def img(only):
    refs = [kie.upload(jpg(FOTOS / "balon-10kg.webp"), "image/jpeg"),
            kie.upload(jpg(FOTOS / "balones-stock.webp", (1600, 1600)), "image/jpeg")]
    tasks = {k: kie.create("nano-banana-2", {"prompt": f"{p} {ESTILO}", "image_input": refs, "aspect_ratio": "9:16",
                                             "resolution": "2K", "output_format": "png"})
             for k, p in IMAGENES.items() if not only or k in only}
    res = kie.wait_all(tasks, timeout=900, every=10)
    log = load()
    for k, r in res.items():
        if r["state"] == "success":
            kie.download(r["urls"][0], OUT / f"{k}.png")
        log[f"img-{k}"] = r
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


def vid(only):
    log = load()
    tasks = {k: kie.create("kling/v2-1-standard", {"prompt": p, "image_url": log[f"img-{k}"]["urls"][0],
                                                   "duration": "5", "negative_prompt": NEG, "cfg_scale": 0.5})
             for k, p in VIDEOS.items() if not only or k in only}
    res = kie.wait_all(tasks, timeout=2400, every=20)
    for k, r in res.items():
        if r["state"] == "success":
            kie.download(r["urls"][0], OUT / f"{k}.mp4")
        log[f"vid-{k}"] = r
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print("créditos antes", kie.credits())
    {"img": img, "vid": vid}[sys.argv[1]](set(sys.argv[2:]))
    print("créditos después", kie.credits())
