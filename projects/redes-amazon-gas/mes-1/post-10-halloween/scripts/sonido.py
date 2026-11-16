"""Música de fondo y efectos del post 10 con ElevenLabs (Music + Sound Effects).

Uso: python3 sonido.py [musica] [sfx]
"""
import json, re, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/audio"
env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
H = {"xi-api-key": KEY, "Content-Type": "application/json"}

MUSICA = ("Playful comedic instrumental for a funny family-friendly TikTok sketch mixing a light Peruvian criollo vals "
          "feel (acoustic guitar and cajon) with a cheeky spooky Halloween touch (pizzicato strings, a little "
          "harpsichord-like plucks), medium tempo, bouncy and warm, not scary, no vocals, simple and sparse so dialogue "
          "sits on top")
SFX = {
    "sfx-llama": ("A home gas stove burner flame sputtering and dying out: soft whoosh, a few weak pops, then "
                  "silence", 2.0),
    "sfx-golpe": ("Short comedic spooky cartoon sting: a playful organ chord and thunder rumble for a funny shocked "
                  "reaction, not scary", 1.8),
}


def post(url, body, dest):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), headers=H)
    try:
        data = urllib.request.urlopen(r, timeout=300).read()
    except urllib.error.HTTPError as e:
        print(dest.name, "HTTP", e.code, e.read()[:300]); return
    dest.write_bytes(data)
    print(dest.name, len(data), "bytes")


what = sys.argv[1:] or ["musica", "sfx"]
if "musica" in what:
    post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
         {"prompt": MUSICA, "music_length_ms": 25000}, OUT / "musica.mp3")
if "sfx" in what:
    for name, (text, dur) in SFX.items():
        post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",
             {"text": text, "duration_seconds": dur, "prompt_influence": 0.5}, OUT / f"{name}.mp3")
