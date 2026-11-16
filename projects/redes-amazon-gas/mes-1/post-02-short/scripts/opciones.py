"""Genera una versión del short por cada música en assets/opciones/.

Para cada canción: salta la intro silenciosa, detecta el pulso con `hyperframes beats`,
coloca cada cambio de lámina en un golpe fuerte (respetando el tiempo mínimo de lectura),
agrega un "swipe" que llega justo en el golpe y renderiza a ../export/opciones-musica/.

Uso: python3 scripts/opciones.py [nombre ...]   (sin nombres: todas)
"""
import json, re, subprocess, sys
from array import array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HF = ["npx", "--yes", "hyperframes@0.8.88"]
OUT = ROOT.parent / "export/opciones-musica"
OUT.mkdir(parents=True, exist_ok=True)

MIN_PORTADA, MIN_PASO, CIERRE = 3.0, 3.8, 2.9  # segundos mínimos por lámina
SWIPE_T = 0.42        # duración del deslizamiento
LAND = 0.21           # el deslizamiento llega a la mitad justo en el golpe


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return array("h", raw)


def rms_db(samples, a, b):
    seg = samples[a:b]
    if not seg:
        return -120
    m = (sum(x * x for x in seg) / len(seg)) ** 0.5
    return 20 * __import__("math").log10(max(m, 1) / 32768)


def arranque(path, umbral=-30):
    """Primer instante (s) en que la música ya suena fuerte."""
    s = pcm(path)
    for i in range(0, len(s), 400):  # ventanas de 50 ms
        if rms_db(s, i, i + 400) > umbral:
            return round(i / 8000, 2)
    return 0.0


def pico(path):
    s = pcm(path)
    i = max(range(len(s)), key=lambda k: abs(s[k]))
    return round(i / 8000, 2)


def elegir_cortes(beats, offset):
    # beats en tiempo de la canción → tiempo del video
    bs = [(b["time"] - offset, b["strength"]) for b in beats if b["time"] - offset > 0.5]
    fuertes = [t for t, st in bs if st >= 0.6] or [t for t, _ in bs]
    todos = [t for t, _ in bs]
    cortes, minimo = [], MIN_PORTADA
    for i in range(4):
        cand = [t for t in fuertes if t >= minimo] or [t for t in todos if t >= minimo]
        t = cand[0] if cand else minimo
        cortes.append(round(t, 3))
        minimo = t + MIN_PASO
    return cortes


def html(musica, offset, cortes, swipe_pico):
    fin = round(cortes[-1] + CIERRE, 2)
    starts = [0] + [round(c - LAND, 3) for c in cortes]
    ends = [round(c - LAND + SWIPE_T, 3) for c in cortes] + [fin]
    colores = ["crema", "marron", "crema", "marron", "crema"]
    slots = "\n".join(
        f'      <div id="sl{i+1}" class="clip slot" data-start="{starts[i]}" data-duration="{round(ends[i]-starts[i],3)}" '
        f'data-track-index="{1 + i % 2}"><div id="pn{i+1}" class="panel {colores[i]}"><img id="im{i+1}" '
        f'src="assets/post-02-slide-{i+1}.png" alt="" /></div></div>' for i in range(5))
    swipes = "\n".join(
        f'      <audio id="swipe{i+1}" src="assets/swipe.mp3" data-start="{round(c - swipe_pico, 3)}" data-duration="0.8" '
        f'data-track-index="{12 + i % 2}" data-volume="0.45"></audio>' for i, c in enumerate(cortes))
    lane = {"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0.7}, {"t": 0.5, "v": 1}, {"t": round(fin - 1.4, 2), "v": 1}, {"t": fin, "v": 0}]}]}
    cuts_js = ",\n".join(f'        [{round(c - LAND, 3)}, {c}, "#pn{i+1}", "#pn{i+2}", "#im{i+2}"]' for i, c in enumerate(cortes))
    breathe = "\n".join(
        f'      tl.fromTo("#im{i+2}", {{ scale: 1.035 }}, {{ scale: 1.0, duration: 0.5, ease: "power2.out" }}, {c});\n'
        f'      tl.fromTo("#pn{i+2}", {{ scale: 1 }}, {{ scale: 1.015, duration: {round(MIN_PASO - 0.6, 2)}, ease: "none" }}, {round(c + 0.5, 3)});'
        for i, c in enumerate(cortes[:3]))
    return f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #fbf8f3; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
      .slot {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
      .slot .panel {{ position: absolute; inset: 0; padding-top: 285px; overflow: hidden; }}
      .crema {{ background: #fbf8f3; }} .marron {{ background: #1b1512; }}
      .slot img {{ display: block; width: 1080px; height: 1350px; }}
    </style>
  </head>
  <body>
    <!-- Generado por scripts/opciones.py con {musica}: cada lámina llega justo en un golpe fuerte de la música. -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{fin}" data-width="1080" data-height="1920">
{slots}
      <audio id="musica" data-timeline-role="music" src="assets/opciones/{musica}.mp3" data-start="0" data-duration="{fin}" data-media-start="{offset}" data-track-index="10" data-volume="0.9"
        data-automation='{json.dumps(lane)}'></audio>
{swipes}
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});

      // Portada: entra con un leve zoom
      tl.fromTo("#im1", {{ scale: 1.06, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.6, ease: "power2.out" }}, 0);

      // Cambio de lámina: [inicio del deslizamiento, golpe, sale, entra, imagen que entra]
      const cuts = [
{cuts_js},
      ];
      for (const [t, beat, out, inn] of cuts) {{
        tl.fromTo(out, {{ x: 0 }}, {{ x: -1080, duration: {SWIPE_T}, ease: "expo.inOut" }}, t);
        tl.fromTo(inn, {{ x: 1080 }}, {{ x: 0, duration: {SWIPE_T}, ease: "expo.inOut" }}, t);
      }}

      // Acento en el golpe y leve respiración mientras se lee
{breathe}
      tl.fromTo("#im5", {{ scale: 1.035 }}, {{ scale: 1.0, duration: 0.5, ease: "power2.out" }}, {cortes[3]});

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""


def main():
    musicas = sys.argv[1:] or sorted(p.stem for p in (ROOT / "assets/opciones").glob("*.mp3"))
    swipe_pico = pico(ROOT / "assets/swipe.mp3")
    resumen = {}
    for m in musicas:
        path = ROOT / f"assets/opciones/{m}.mp3"
        offset = arranque(path)
        # primero una composición provisional para que `beats` encuentre la pista
        (ROOT / "index.html").write_text(html(m, offset, [3.5, 7.5, 11.5, 15.5], swipe_pico))
        subprocess.run(HF + ["beats", "--json", "."], cwd=ROOT, capture_output=True, check=True)
        beats = json.loads((ROOT / f"beats/assets/opciones/{m}.mp3.json").read_text())["beats"]
        cortes = elegir_cortes(beats, offset)
        (ROOT / "index.html").write_text(html(m, offset, cortes, swipe_pico))
        chk = subprocess.run(HF + ["check"], cwd=ROOT, capture_output=True, text=True)
        ok = "Check passed" in chk.stdout + chk.stderr
        subprocess.run(HF + ["render", "-o", str(OUT / f"post-02-short-{m}.mp4")], cwd=ROOT, capture_output=True, check=True)
        bpm = round(60 / ((beats[-1]["time"] - beats[0]["time"]) / (len(beats) - 1)), 1) if len(beats) > 1 else None
        resumen[m] = {"offset": offset, "cortes": cortes, "fin": round(cortes[-1] + CIERRE, 2), "pulsos": len(beats), "bpm_detectado": bpm, "check": ok}
        (ROOT / f"variantes/index.{m}.html").write_text((ROOT / "index.html").read_text())
        print(m, resumen[m], flush=True)
    (OUT / "resumen.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
