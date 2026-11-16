"""Voz en off del post 8 con ElevenLabs (Terry), con timestamps por carácter. Mismo patrón que post-01-rio."""
import base64, json, re, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/audio"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
VOICE = "ulJB4yAMefhHYn0FWgGy"  # Terry — masculina, peruana (elegida por Enzo)

TEXTO = (
    "¿Huele a gas en tu casa? Tranquilo. Haz esto en cuatro pasos. "
    "Uno: no prendas ni apagues luces ni aparatos. Y nada de fósforos. "
    "Dos: abre puertas y ventanas. "
    "Tres: cierra la válvula del balón. "
    "Cuatro: sal de la casa y, ya afuera, llama a los bomberos al uno, uno, seis. "
    "Guarda este video y compártelo con tu familia."
)

body = {
    "text": TEXTO,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.2, "use_speaker_boost": True},
}
for espera in (0, 30, 60, 120):
    time.sleep(espera)
    try:
        r = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
            data=json.dumps(body).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        d = json.loads(urllib.request.urlopen(r, timeout=180).read())
        break
    except urllib.error.HTTPError as e:
        if e.code != 429:
            raise
        print("429, reintento")
(OUT / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
(OUT / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
print("chars", len(TEXTO), "dur", d["alignment"]["character_end_times_seconds"][-1])
