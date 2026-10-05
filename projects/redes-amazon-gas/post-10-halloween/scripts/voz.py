"""Diálogo de Doña Meche (post 10, Halloween + Canción Criolla) con ElevenLabs, una pista por plano, con timestamps.

Voz: "Lily" (voz peruana femenina, adulta, enérgica) de la librería compartida de ElevenLabs.
Uso: python3 voz.py [a b c]
"""
import base64, json, re, sys, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[2]
OUT = ROOT / "assets/audio"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
VOICE = "ek0qR5Bu0N3aPdijsdae"  # Lily — femenina, peruana, adulta, cálida y enérgica (Doña Meche)

LINEAS = {
    "a": "Sábado de jarana criolla y Halloween. ¿Brujas? ¿Fantasmas? A mí nada me asusta, vecina.",
    "b": "¡Ay, no, otra vez no! ¿Se acabó el gas? ¡Esto sí da miedo!",
    "c": "El susto más grande de Iquitos es quedarse sin gas el sábado. Pide antes a Amazon Gas por WhatsApp.",
}
SETTINGS = {"stability": 0.35, "similarity_boost": 0.8, "style": 0.5, "use_speaker_boost": True}


def tts(key, text):
    body = {"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": SETTINGS}
    r = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(r, timeout=180).read())
    (OUT / f"voz-{key}.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / f"voz-{key}-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
    print(key, "chars", len(text), "dur", d["alignment"]["character_end_times_seconds"][-1])


only = sys.argv[1:] or list(LINEAS)
for k in only:
    try:
        tts(k, LINEAS[k])
    except urllib.error.HTTPError as e:
        print(k, "HTTP", e.code, e.read()[:300])
