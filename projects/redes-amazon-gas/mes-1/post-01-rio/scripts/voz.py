"""Voz en off del post 1 con ElevenLabs (voz peruana "Terry"), con timestamps por carácter."""
import base64, json, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/audio"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
VOICE = "ulJB4yAMefhHYn0FWgGy"  # Terry — masculina, peruana, narración suave (elegida por Enzo)

TEXTO = (
    "Iquitos no tiene carretera. Entonces... ¿cómo llega el gas a tu cocina? "
    "Por el río. Nuestras barcazas transportan el gas a granel por la Amazonía. "
    "En nuestra planta de Santa Clara de Nanay lo envasamos con seguridad. "
    "Y de ahí, directo a tu casa. "
    "Amazon Gas: la energía que mueve a Loreto, desde el año dos mil."
)

body = {
    "text": TEXTO,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True},
}
r = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
    data=json.dumps(body).encode(), headers={"xi-api-key": KEY, "Content-Type": "application/json"})
d = json.loads(urllib.request.urlopen(r, timeout=180).read())
(OUT / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
(OUT / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
print("chars", len(TEXTO), "dur", d["alignment"]["character_end_times_seconds"][-1])
