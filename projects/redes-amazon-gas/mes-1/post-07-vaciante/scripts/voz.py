"""Post 7 (vaciante): voz en off con ElevenLabs (Terry) con timestamps por carácter, y música de fondo.

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

# Parte 2 de "Iquitos no tiene carretera" (post 1). Sin cifras ni cantidad de embarcaciones (pedido de Enzo, 2026-10-21).
TEXTO = (
    "Iquitos no tiene carretera. Y en la vaciante, el río tampoco ayuda. "
    "¿Cómo llega el gas cuando el río baja? "
    "Desde la barcaza seguimos navegando, con cuidado y con experiencia. "
    "Porque el gas tiene que llegar a tu cocina. "
    "Amazon Gas, energía que mueve a Loreto."
)

MUSICA = ("Calm, warm cinematic documentary underscore inspired by the Amazon river at dawn: soft acoustic guitar "
          "and gentle marimba, light shaker, subtle low strings, steady hopeful pulse around 90 bpm, no vocals, "
          "builds slightly toward the end and resolves cleanly.")


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
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True},
    }
    d = json.loads(post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", body))
    (OUT / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
    print("voz chars", len(TEXTO), "dur", d["alignment"]["character_end_times_seconds"][-1])


def musica():
    audio = post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                 {"prompt": MUSICA, "music_length_ms": 22000})
    (OUT / "musica.mp3").write_bytes(audio)
    print("musica bytes", len(audio))


if __name__ == "__main__":
    que = set(sys.argv[1:]) or {"voz", "musica"}
    if "voz" in que:
        voz()
    if "musica" in que:
        musica()
