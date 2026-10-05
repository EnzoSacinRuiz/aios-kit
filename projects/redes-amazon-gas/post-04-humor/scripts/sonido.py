"""Música de fondo y efectos del post 4 con ElevenLabs (Music + Sound Effects).

Uso: python3 sonido.py [musica] [sfx]
"""
import json, re, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[2]
OUT = ROOT / "assets/audio"
env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
H = {"xi-api-key": KEY, "Content-Type": "application/json"}

MUSICA = ("Playful light comedic Amazonian cumbia instrumental for a funny TikTok sketch, cheerful electric guitar "
          "melody, guiro and soft percussion, medium tempo, bouncy and warm, no vocals, simple and not too busy so "
          "dialogue sits on top")
SFX = {
    "sfx-llama": ("A home gas stove burner flame sputtering and dying out: soft whoosh, a few weak pops, then "
                  "silence", 2.0),
    "sfx-golpe": ("Short comedic cartoon dramatic sting, quick orchestral 'dun dun dun' hit for a funny shocked "
                  "reaction", 1.6),
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
         {"prompt": MUSICA, "music_length_ms": 26000}, OUT / "musica.mp3")
if "sfx" in what:
    for name, (text, dur) in SFX.items():
        post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",
             {"text": text, "duration_seconds": dur, "prompt_influence": 0.5}, OUT / f"{name}.mp3")
