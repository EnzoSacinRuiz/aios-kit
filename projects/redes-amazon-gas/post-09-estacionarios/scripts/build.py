"""Arma index.html (composición HyperFrames 1080x1920) a partir de la alineación de la voz.

Uso: python3 scripts/build.py
Para cambiar el número de WhatsApp del cierre, edita WHATSAPP y vuelve a correr + renderizar.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WHATSAPP = "[WhatsApp]"   # número pendiente de confirmar
OFF = 0.3                 # la voz arranca a los 0.3 s
TOTAL = 20.0
END = 14.0                # entra la placa de cierre

a = json.loads((ROOT / "assets/audio/voz-alignment.json").read_text())
words, w, ws, pe = [], "", None, 0
for ch, st, en in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if ch == " ":
        if w:
            words.append((w, ws + OFF, pe + OFF))
            w = ""
        continue
    if not w:
        ws = st
    w += ch
    pe = en
if w:
    words.append((w, ws + OFF, pe + OFF))
VOZ_DUR = round(a["character_end_times_seconds"][-1] + 0.2, 2)

# Agrupa en frases cortas de subtítulo: corta en puntuación o a las 3 palabras
groups, cur = [], []
for wd in words:
    cur.append(wd)
    if wd[0][-1] in ".,?" or len(cur) == 3:
        groups.append(cur)
        cur = []
if cur:
    groups.append(cur)
groups = [g for g in groups if g[0][1] < END]  # el cierre no lleva subtítulos

cap_html, cap_js = [], []
for i, g in enumerate(groups):
    start = g[0][1]
    nxt = groups[i + 1][0][1] if i + 1 < len(groups) else min(g[-1][2] + 0.3, END)
    dur = round(min(nxt, END) - start, 2)
    spans = " ".join(f'<span class="w" id="w{i}_{j}">{x[0]}</span>' for j, x in enumerate(g))
    cap_html.append(f'      <div id="cap{i}" class="clip cap" data-start="{start:.2f}" data-duration="{dur}" '
                    f'data-track-index="4"><div class="cap-in">{spans}</div></div>')
    cap_js.append(f'      tl.fromTo("#cap{i} .cap-in", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {start:.2f});')
    for j, x in enumerate(g):
        cap_js.append(f'      tl.fromTo("#w{i}_{j}", {{ color: "#fbf8f3" }}, {{ color: "#f5dc17", duration: 0.06 }}, {x[1]:.2f});')

html = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Barlow Condensed"; font-weight: 600; src: url("assets/fonts/BarlowCondensed-SemiBold.ttf") format("truetype"); }}
      @font-face {{ font-family: "Barlow Condensed"; font-weight: 700; src: url("assets/fonts/BarlowCondensed-Bold.ttf") format("truetype"); }}
      @font-face {{ font-family: "Barlow Condensed"; font-weight: 800; src: url("assets/fonts/BarlowCondensed-ExtraBold.ttf") format("truetype"); }}
      @font-face {{ font-family: "Inter"; font-weight: 100 900; src: url("assets/fonts/Inter.ttf") format("truetype"); }}
      :root {{ --granate: #8e4149; --granate-oscuro: #6e2f35; --marron: #1b1512; --crema: #fbf8f3; --arena: #c9bdb0; --llama: #f5dc17; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--marron); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; }}
      .shot-wrap {{ position: absolute; inset: 0; overflow: hidden; }}
      img.still {{ position: absolute; top: 0; left: 0; height: 100%; width: auto; max-width: none; }}
      video.shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #veil {{ position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(27,21,18,0.62) 0%, rgba(27,21,18,0.08) 40%, rgba(27,21,18,0.08) 55%, rgba(27,21,18,0.62) 100%); }}
      .card {{ position: absolute; left: 80px; right: 150px; top: 280px; }}
      .kicker {{ display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 44px;
        letter-spacing: 0.08em; text-transform: uppercase; color: var(--crema); background: var(--granate); padding: 6px 18px 4px; }}
      .headline {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase; color: var(--crema);
        font-size: 132px; line-height: 0.9; letter-spacing: -0.01em; text-shadow: 0 4px 24px rgba(27,21,18,0.6); margin-top: 18px; }}
      .headline em {{ font-style: normal; color: var(--llama); }}
      .sub {{ margin-top: 26px; max-width: 780px; font-weight: 600; font-size: 44px; line-height: 1.2; color: var(--crema);
        text-shadow: 0 2px 14px rgba(27,21,18,0.8); }}
      .bar {{ display: block; width: 140px; height: 12px; background: var(--granate); margin-top: 26px; }}
      .cap {{ position: absolute; left: 70px; right: 150px; top: 1200px; }}
      .cap-in {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 84px; line-height: 1.02; text-transform: uppercase;
        color: var(--crema); text-shadow: 0 3px 0 rgba(27,21,18,0.9), 0 0 22px rgba(27,21,18,0.85); }}
      .cap-in .w {{ display: inline-block; }}
      #end {{ position: absolute; inset: 0; background: var(--crema); display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #end-logo {{ width: 360px; height: auto; display: block; }}
      #end-tag {{ margin-top: 60px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase; font-size: 100px;
        line-height: 0.95; color: var(--marron); text-align: center; max-width: 880px; }}
      #end-tag em {{ font-style: normal; color: var(--granate); }}
      #end-list {{ margin-top: 40px; font-weight: 600; font-size: 40px; color: #6b5d51; text-align: center; line-height: 1.45; }}
      #end-cta {{ margin-top: 64px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase; font-size: 64px;
        color: var(--crema); background: var(--granate); padding: 14px 40px 10px; }}
      #end-rule {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: var(--granate); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Fotos reales animadas con kie.ai (Kling 2.1); fundido de 0.4 s entre tomas -->
      <div id="v1-vis" class="shot-wrap"><video id="v1" class="clip shot" src="assets/clips/s1-bateria.mp4" data-start="0" data-duration="4.5" data-track-index="0" muted playsinline></video></div>
      <div id="v2-vis" class="shot-wrap"><img id="v2" class="clip still" src="assets/img/estacionarios-1.jpg" alt="" data-start="4.1" data-duration="5.0" data-track-index="1" /></div>
      <div id="v3-vis" class="shot-wrap"><video id="v3" class="clip shot" src="assets/clips/s3-azotea.mp4" data-start="8.9" data-duration="2.6" data-track-index="0" muted playsinline></video></div>
      <div id="v4-vis" class="shot-wrap"><video id="v4" class="clip shot" src="assets/clips/s4-cisterna.mp4" data-start="11.1" data-duration="3.3" data-track-index="1" muted playsinline></video></div>
      <div id="veil" class="clip" data-start="0" data-duration="{END + 0.4}" data-track-index="2"></div>

      <div id="t1" class="clip card" data-start="0.2" data-duration="1.9" data-track-index="3">
        <div class="t1-in"><span class="kicker">Negocios</span><div class="headline">¿Restaurante o panadería?</div></div>
      </div>
      <div id="t2" class="clip card" data-start="2.2" data-duration="2.0" data-track-index="3">
        <div class="t2-in"><div class="headline">No cambies más <em>balones</em></div><span class="bar"></span></div>
      </div>
      <div id="t3" class="clip card" data-start="4.3" data-duration="4.8" data-track-index="3">
        <div class="t3-in"><span class="kicker">Tanque estacionario</span><div class="headline">Desde 80 galones</div>
          <div class="sub t3-sub">Gas de corrido para tu negocio.</div></div>
      </div>
      <div id="t4" class="clip card" data-start="9.6" data-duration="1.5" data-track-index="3">
        <div class="t4-in"><div class="headline">Lo instalamos</div><span class="bar"></span></div>
      </div>
      <div id="t5" class="clip card" data-start="11.1" data-duration="2.9" data-track-index="3">
        <div class="t5-in"><span class="kicker">Con nuestra cisterna</span><div class="headline">Lo llenamos en tu local</div></div>
      </div>

      <!-- Subtítulos (alineación de la voz de Terry) -->
{chr(10).join(cap_html)}

      <div id="end" class="clip" data-start="{END}" data-duration="{TOTAL - END}" data-track-index="5">
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-tag">Tu negocio, con gas <em>de corrido</em></div>
        <div id="end-list">Restaurantes · Panaderías · Hoteles · Industria</div>
        <div id="end-cta">Cotiza al {WHATSAPP}</div>
        <div id="end-rule"></div>
      </div>

      <audio id="musica" src="assets/audio/musica.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="0.5"
        data-automation='{{"version":1,"lanes":[{{"target":"volume","points":[{{"t":0,"v":0}},{{"t":0.5,"v":0.45}},{{"t":15.2,"v":0.45}},{{"t":15.8,"v":1}},{{"t":18.6,"v":1}},{{"t":{TOTAL},"v":0}}]}}]}}'></audio>
      <audio id="voz" src="assets/audio/voz.mp3" data-start="{OFF}" data-duration="{VOZ_DUR}" data-track-index="10" data-volume="1"></audio>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      const E = "power3.out";
      const up = (sel, t, y = 60, d = 0.4) => tl.fromTo(sel, {{ opacity: 0, y }}, {{ opacity: 1, y: 0, duration: d, ease: E }}, t);

      up("#t1 .kicker", 0.2, 30, 0.3); up("#t1 .headline", 0.25);
      tl.to("#t1 .t1-in", {{ opacity: 0, duration: 0.2 }}, 1.95);
      up("#t2 .headline", 2.2);
      tl.fromTo("#t2 .bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: E }}, 2.45);
      tl.to("#t2 .t2-in", {{ opacity: 0, duration: 0.2 }}, 4.0);
      up("#t3 .kicker", 4.3, 30, 0.3); up("#t3 .headline", 6.55); up("#t3 .t3-sub", 7.9, 24, 0.35);
      tl.to("#t3 .t3-in", {{ opacity: 0, duration: 0.2 }}, 8.9);
      up("#t4 .headline", 9.6);
      tl.fromTo("#t4 .bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: E }}, 9.85);
      tl.to("#t4 .t4-in", {{ opacity: 0, duration: 0.2 }}, 10.9);
      up("#t5 .kicker", 11.3, 30, 0.3); up("#t5 .headline", 11.9);

      tl.fromTo("#v2-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, 4.1);
      // Tanques: foto real (sin IA) con paneo lento hacia el logo del tanque delantero
      tl.fromTo("#v2", {{ x: -620, scale: 1.0 }}, {{ x: -1060, scale: 1.06, duration: 5.0, ease: "none", transformOrigin: "50% 50%" }}, 4.1);
      tl.fromTo("#v3-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, 8.9);
      tl.fromTo("#v4-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, 11.1);
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {END});

      tl.fromTo("#end-logo", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {END + 0.05});
      tl.fromTo("#end-rule", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {END + 0.2});
      up("#end-tag", {END + 0.5}, 40, 0.5);
      up("#end-list", {END + 0.9}, 20, 0.4);
      tl.fromTo("#end-cta", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }}, {END + 1.4});

      // Subtítulos: la palabra dicha se enciende en amarillo llama
{chr(10).join(cap_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(html)
print("index.html OK", len(groups), "subtítulos; voz", VOZ_DUR, "s")
