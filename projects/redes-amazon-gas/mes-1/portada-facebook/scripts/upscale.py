"""Mejora la foto real de la barcaza (WhatsApp, 1386x640) con upscale en kie.ai. No la regenera: mismo contenido.

Uso: python3 scripts/upscale.py  → assets/barcaza-sol-upscale-<modelo>.png
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "post-04-humor/scripts"))
import kie  # noqa: E402

src = ROOT / "assets/barcaza-sol-original.png"
print("créditos antes", kie.credits())
url = kie.upload(src, "image/png")
tareas = {}
for nombre, model, inp in [
    ("topaz", "topaz/image-upscale", {"image_url": url, "upscale_factor": "2"}),
    ("recraft", "recraft/crisp-upscale", {"image": url}),
]:
    try:
        tareas[nombre] = kie.create(model, inp)
    except Exception as e:  # noqa: BLE001
        print(nombre, "no se pudo crear:", e)
res = kie.wait_all(tareas, timeout=900)
for nombre, r in res.items():
    if r["state"] == "success":
        kie.download(r["urls"][0], ROOT / f"assets/barcaza-sol-upscale-{nombre}.png")
    print(nombre, r)
print("créditos después", kie.credits())
