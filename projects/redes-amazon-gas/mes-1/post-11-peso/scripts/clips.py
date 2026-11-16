"""Post 11 (peso verificado): imágenes y clips con kie.ai.

- img: Nano Banana 2 genera las escenas de planta (balanza, precinto, línea de llenado) usando como
  referencia las fotos reales del balón de 10 kg y del stock, para que el balón sea el de Amazon Gas.
  La balanza NO muestra números legibles: el peso va como gráfico en HyperFrames.
- vid: Kling 2.1 Standard anima esas imágenes y la foto real del camión de reparto.

Uso: python3 scripts/clips.py img | vid [ids...]
"""
import io, json, sys
from PIL import Image
import kie

ROOT = kie.ROOT
FOTOS = kie.AIOS / "references/branding/fotos"
OUT = ROOT / "assets/clips"
OUT.mkdir(parents=True, exist_ok=True)
LOG = OUT / "credits.json"

ESTILO = ("Photorealistic documentary photo, vertical 9:16, natural daylight in an LPG bottling plant in the Peruvian "
          "Amazon (Iquitos), clean industrial look, shallow depth of field. The gas cylinder is exactly the brown "
          "10 kg AMAZON GAS cylinder from the reference: brown body, yellow triangle logo with flame, white 'AMAZON "
          "GAS' text. No other brands. No readable numbers on any display.")
IMAGENES = {
    "a-balanza": "A single brown AMAZON GAS 10 kg cylinder standing on a stainless steel industrial platform scale, "
                 "the digital scale display is visible but out of focus, a worker's gloved hand steadies the valve, "
                 "rows of brown cylinders blurred in the background.",
    "b-precinto": "Close-up of a worker's gloved hands placing a yellow plastic security seal over the valve of a "
                  "brown AMAZON GAS cylinder, the label on the shoulder is visible, other cylinders blurred behind.",
    "c-llenado": "An LPG cylinder filling line: several brown AMAZON GAS cylinders in a row on a conveyor, each "
                 "connected to a filling head with a hose, a worker in blue uniform and yellow helmet checks them, "
                 "wide shot.",
}
VIDEOS = {  # id: (fuente, prompt)
    "a-balanza": ("img", "Slow cinematic push-in toward the gas cylinder standing on the scale, the gloved hand lets "
                         "go, subtle background movement, realistic, keep the logo and cylinder unchanged."),
    "b-precinto": ("img", "The gloved hands press the plastic seal down over the valve and pull away, slow and "
                          "steady, realistic, keep the logo unchanged."),
    "c-llenado": ("img", "The conveyor moves slowly to the left carrying the cylinders, the worker checks a filling "
                         "head, slow lateral camera move, realistic, keep logos unchanged."),
    "d-camion": ("camion-balones", "The truck loaded with gas cylinders starts driving slowly to the left, trees "
                                   "move lightly in the wind, stable camera, realistic, keep the truck, signs and "
                                   "cylinders unchanged."),
}
NEG = "blur, distortion, warped text, deformed logo, extra objects, morphing, readable numbers, low quality"


def jpg(path, size=None, crop916=False, cx=0.5):
    im = Image.open(path).convert("RGB")
    if crop916:
        w, h = im.size
        cw = int(h * 9 / 16)
        left = max(0, min(w - cw, int(cx * w - cw / 2)))
        im = im.crop((left, 0, left + cw, h)).resize((720, 1280), Image.LANCZOS)
    elif size:
        im.thumbnail(size)
    dest = OUT / f"{path.stem}.jpg"
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
    tasks = {}
    for k, (src, prompt) in VIDEOS.items():
        if only and k not in only:
            continue
        if src == "img":
            url = log[f"img-{k}"]["urls"][0]
        else:
            url = kie.upload(jpg(FOTOS / f"{src}.webp", crop916=True, cx=0.45), "image/jpeg")
        tasks[k] = kie.create("kling/v2-1-standard", {"prompt": prompt, "image_url": url, "duration": "5",
                                                      "negative_prompt": NEG, "cfg_scale": 0.5})
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
