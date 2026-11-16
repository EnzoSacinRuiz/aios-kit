"""Mes 2, post 1 (precinto): voz en off con ElevenLabs (Terry) con timestamps por carácter, y música de fondo.

Uso: python3 scripts/voz.py [voz] [musica]   (sin argumentos: las dos)
"""
import base64, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/audio"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
VOICE = "ulJB4yAMefhHYn0FWgGy"  # Terry — masculina, peruana, narración suave (elegida por Enzo)

# El precinto dice "Amazon Gas" (Enzo, 2026-11-15).
TEXTO = (  # versión B, más informativa y neutral (Enzo, 2026-11-16)
    "Para saber si tu balón es Amazon Gas, fíjate en el precinto. "
    "Todos nuestros balones salen de planta con su precinto amarillo y nuestro nombre impreso. "
    "Si el precinto no es amarillo, no dice Amazon Gas o está roto, ese balón no salió así de nuestra planta. "
    "Te recomendamos no recibirlo. "
    "Si tienes dudas, mándanos una foto del precinto por WhatsApp."
)

MUSICA = ("Warm, confident and modern documentary underscore for a home safety brand video: light percussion, "
          "clean plucked guitar and soft marimba, subtle bass, steady trustworthy pulse around 100 bpm, no vocals, "
          "a brief tense pause feel in the middle, resolves warmly at the end.")


def post(url, body, tries=4):
    wait = 30
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=json.dumps(body).encode(),
                                       headers={"xi-api-key": KEY, "Content-Type": "application/json"})
            return urllib.request.urlopen(r, timeout=300).read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                print("429, espero", wait, flush=True)
                time.sleep(wait)
                wait = min(wait * 2, 120)
                continue
            print(e.code, e.read()[:400])
            raise


def voz():
    body = {
        "text": TEXTO,
        "model_id": "eleven_multilingual_v2",
        # style 0 y stability 0.65: tono neutral e informativo, no de profesor (Enzo, 2026-11-16)
        "voice_settings": {"stability": 0.65, "similarity_boost": 0.8, "style": 0.0, "use_speaker_boost": True,
                           "speed": 0.95},  # 0.88 se sentía lenta (Enzo, 2026-11-15); a 1.0 sonaba acelerada (2026-10-26)
    }
    d = json.loads(post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", body))
    (OUT / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
    print("voz chars", len(TEXTO), "dur", d["alignment"]["character_end_times_seconds"][-1])


def musica():
    audio = post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                 {"prompt": MUSICA, "music_length_ms": 30000})
    (OUT / "musica.mp3").write_bytes(audio)
    print("musica bytes", len(audio))


if __name__ == "__main__":
    que = set(sys.argv[1:]) or {"voz", "musica"}
    if "voz" in que:
        voz()
    if "musica" in que:
        musica()
