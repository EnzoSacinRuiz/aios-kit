"""Voz en off (Terry) y música del post 5 con ElevenLabs.

Uso: python3 scripts/audio.py voz | musica   (sin argumento: ambas)
Guarda assets/audio/voz.mp3, voz-alignment.json, musica.mp3 y audio-log.json (caracteres usados).
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

TEXTO = (
    "¿Sabes qué hay detrás de cada balón que llega a tu casa? Gente que entrena. "
    "Simulacros contra incendios en nuestra planta. "
    "Prácticas con mangueras, junto a las barcazas. "
    "Así nos preparamos... para que tú cocines tranquilo. "
    "Amazon Gas: seguridad desde el año dos mil."
)

MUSICA = ("Warm, hopeful instrumental background track for a short corporate safety video from the Peruvian Amazon. "
          "Soft acoustic guitar and light marimba with gentle percussion, steady mid tempo around 100 bpm, "
          "uplifting and trustworthy, no vocals, builds slightly and ends cleanly.")


def post(url, body, raw=False, tries=4):
    wait = 30
    for i in range(tries):
        try:
            r = urllib.request.Request(url, data=json.dumps(body).encode(),
                                       headers={"xi-api-key": KEY, "Content-Type": "application/json"})
            resp = urllib.request.urlopen(r, timeout=300)
            return resp.read() if raw else json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                print("429, espero", wait, flush=True)
                time.sleep(wait)
                wait *= 2
                continue
            print(e.code, e.read()[:400])
            raise


def voz(log):
    body = {"text": TEXTO, "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.25, "use_speaker_boost": True}}
    d = post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", body)
    (OUT / "voz.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    (OUT / "voz-alignment.json").write_text(json.dumps(d["alignment"], ensure_ascii=False))
    log["voz"] = {"chars": len(TEXTO), "dur": d["alignment"]["character_end_times_seconds"][-1]}
    print("voz", log["voz"])


def musica(log):
    audio = post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                 {"prompt": MUSICA, "music_length_ms": 22000}, raw=True)
    (OUT / "musica.mp3").write_bytes(audio)
    log["musica"] = {"length_ms": 22000, "bytes": len(audio)}
    print("musica", log["musica"])


def usage():
    try:
        r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": KEY})
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
        return {"character_count": d.get("character_count"), "character_limit": d.get("character_limit")}
    except Exception as e:  # noqa: BLE001
        return f"err {e}"


if __name__ == "__main__":
    which = sys.argv[1:] or ["voz", "musica"]
    lf = OUT / "audio-log.json"
    log = json.loads(lf.read_text()) if lf.exists() else {}
    log.setdefault("runs", []).append({"which": which, "before": usage()})
    for w in which:
        globals()[w](log)
    log["runs"][-1]["after"] = usage()
    print("uso", log["runs"][-1])
    lf.write_text(json.dumps(log, indent=2, ensure_ascii=False))
