"""Opciones de música de fondo del post 8 con ElevenLabs Music.

La música original sonaba a película de terror. Estas opciones buscan calma y confianza:
el video es de seguridad, debe tranquilizar, no asustar.

Uso: python3 scripts/musica.py [a] [b] [c]   → assets/audio/opciones/musica-<x>.mp3
"""
import json, re, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/audio/opciones"
OUT.mkdir(parents=True, exist_ok=True)
env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
H = {"xi-api-key": KEY, "Content-Type": "application/json"}

BASE = ("instrumental, no vocals, major key, calm and reassuring, never dark, never suspenseful, no horror, "
        "no drones, simple and not too busy so a voice-over sits clearly on top")
OPCIONES = {
    "a": "Warm acoustic guitar fingerpicking with light shaker, friendly public-service announcement feel, "
         "gentle steady tempo around 95 bpm, " + BASE,
    "b": "Soft mellow Amazonian cumbia, clean electric guitar and light guiro, relaxed low-energy groove, "
         "warm and friendly neighbourhood feel, " + BASE,
    "c": "Light uplifting piano with soft pads and a subtle steady pulse, clear informative tutorial feel, "
         "positive and confident, " + BASE,
}

for k in sys.argv[1:] or list(OPCIONES):
    r = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                               data=json.dumps({"prompt": OPCIONES[k], "music_length_ms": 25000}).encode(), headers=H)
    try:
        data = urllib.request.urlopen(r, timeout=300).read()
    except urllib.error.HTTPError as e:
        print(k, "HTTP", e.code, e.read()[:300]); continue
    (OUT / f"musica-{k}.mp3").write_bytes(data)
    print(k, len(data), "bytes")
