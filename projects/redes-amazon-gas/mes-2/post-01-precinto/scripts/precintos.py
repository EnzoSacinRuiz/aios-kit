"""Fotos reales del precinto (image copy 7/8/9.png, de Enzo): recorte 9:16 con el precinto centrado
en horizontal y upscale x2 con Topaz en kie.ai. Si el upscale falla, se queda el recorte con lanczos.

Uso: python3 scripts/precintos.py
"""
import json
from pathlib import Path
from PIL import Image, ImageFilter

import kie

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets/img"
# nombre de salida: (archivo original, centro x del precinto en el original)
FOTOS = {
    "precinto-1": ("image copy 8.png", 530),   # toma 2: "Míralo en el precinto"
    "precinto-2": ("image copy 9.png", 544),   # toma 3b: checks
    "precinto-3": ("image copy 7.png", 549),   # fondo de "No lo recibas"
}
W, H = 900, 1600  # 9:16 a toda la altura de la foto (1200x1600)

tasks, crops = {}, {}
for name, (src, cx) in FOTOS.items():
    im = Image.open(ROOT / src).convert("RGB")
    x0 = max(0, min(cx - W // 2, im.width - W))
    crop = im.crop((x0, 0, x0 + W, H))
    p = IMG / f"{name}-crop.jpg"
    crop.save(p, quality=95)
    crops[name] = crop
    url = kie.upload(p, "image/jpeg")
    tasks[name] = kie.create("topaz/image-upscale", {"image_url": url, "upscale_factor": "2"})
    print(name, "subido", flush=True)

res = kie.wait_all(tasks, timeout=900, every=10)
for name, r in res.items():
    out = IMG / f"{name}.jpg"
    if r["state"] == "success":
        tmp = IMG / f"{name}-up.png"
        kie.download(r["urls"][0], tmp)
        Image.open(tmp).convert("RGB").resize((1620, 2880), Image.LANCZOS).save(out, quality=92)
        tmp.unlink()
    else:
        crops[name].resize((1620, 2880), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 80, 2)).save(out, quality=92)
    print(name, r["state"], r.get("credits"), "->", out.name)
(ROOT / "assets/img/precintos-kie.json").write_text(json.dumps(res, indent=1))
