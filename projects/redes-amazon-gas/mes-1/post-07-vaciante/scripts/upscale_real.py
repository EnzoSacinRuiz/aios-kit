"""Mejora el video real de la barcaza (WhatsApp, 854x480, 9,3 s) con upscale Topaz x2. No lo regenera: mismo contenido.

El 2026-10-21, topaz/video-upscale en kie.ai falló 3 veces ("internal error", sin cobrar créditos), así que se usa
Topaz en fal.ai. kie.ai solo se usa para alojar el archivo y darle una URL pública.
Uso: python3 scripts/upscale_real.py  → assets/clips/real-barcaza-upscale.mp4 (1708x960, 30 fps)
"""
import json, re, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / "post-04-humor/scripts"))
import kie  # noqa: E402

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (kie.AIOS / ".env").read_text(), re.M))
H = {"Authorization": f"Key {env['FAL_AI_API_KEY'].strip().strip(chr(34))}", "Content-Type": "application/json"}

RAW = ROOT.parent / "raw/VID-20261006-WA0011.mp4"
shutil.copyfile(RAW, ROOT / "assets/clips/real-barcaza-original.mp4")
# El framerate variable de WhatsApp se normaliza a 30 fps constantes antes de subirlo.
src = ROOT / "assets/clips/real-barcaza-cfr.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(RAW), "-vf", "fps=30", "-c:v", "libx264", "-crf", "14",
                "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(src)], check=True)


def fal(url, data=None):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None, headers=H)
    return json.loads(urllib.request.urlopen(r, timeout=120).read())


job = fal("https://queue.fal.run/fal-ai/topaz/upscale/video", {"video_url": kie.upload(src, "video/mp4"), "upscale_factor": 2})
while fal(job["status_url"]).get("status") != "COMPLETED":
    time.sleep(10)
out = fal(job["response_url"])["video"]["url"]
urllib.request.urlretrieve(out, ROOT / "assets/clips/real-barcaza-upscale.mp4")
print("ok", job["request_id"], out)
