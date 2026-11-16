"""Post 3: voz en off (Terry, ElevenLabs) con timestamps por carácter + música de fondo.

Uso: python3 scripts/voz.py [voz] [musica]   (sin args: ambas)
"""
import base64, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[3]
OUT = ROOT / "assets/audio"
OUT.mkdir(parents=True, exist_ok=True)

env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["ELEVENLABS_API_KEY"].strip().strip('"')
VOICE = "ulJB4yAMefhHYn0FWgGy"  # Terry — voz de marca

B = ' <break time="0.8s" /> '  # pausa para leer cada paso en pantalla
TEXTO = (
    "¿Tacacho con cecina para el desayuno? Así sale bien." + B +
    "Pela el plátano verde y córtalo en trozos." + B +
    "Fríelo a fuego parejo, sin apuro, hasta que esté doradito." + B +
    "Machácalo con un poquito de manteca, chicharrón y su sal." + B +
    "Forma tus bolitas con la mano." + B +
    "Mientras, dora la cecina en la sartén, vuelta y vuelta." + B +
    "Y listo: el desayuno loretano de siempre." + B +
    "Y a ti, ¿cuál es tu plato loretano favorito? Cuéntanos en los comentarios."
)

MUSICA = ("Warm, light Amazonian Peruvian cumbia instrumental for a home cooking video, soft guitars, gentle "
          "percussion, cheerful morning mood, relaxed tempo, no vocals, background bed under a voiceover")


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
                wait *= 2
                continue
            print("HTTP", e.code, e.read()[:400], flush=True)
            raise


def voz():
    body = {"text": TEXTO, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True}}
    d = json.loads(post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps"
                        "?output_format=mp3_44100_128", body))
    (OUT / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
    print("voz chars", len(TEXTO), "dur", d["alignment"]["character_end_times_seconds"][-1])


def musica():
    audio = post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                 {"prompt": MUSICA, "music_length_ms": 42000})
    (OUT / "musica.mp3").write_bytes(audio)
    print("musica bytes", len(audio))


if __name__ == "__main__":
    which = set(sys.argv[1:]) or {"voz", "musica"}
    if "voz" in which:
        voz()
    if "musica" in which:
        musica()
