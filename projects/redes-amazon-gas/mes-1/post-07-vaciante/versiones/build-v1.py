"""Genera index.html del post 7 (vaciante) a partir de la alineación de la voz de Terry.

Mismo lenguaje visual que post-01-rio (Barlow Condensed, granate/crema, subtítulos palabra a palabra
en amarillo llama), con otras tomas y otro cierre.
Uso: python3 scripts/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO = 0.30          # la voz entra 0.3 s después del inicio
END = 11.65        # entra el cierre (justo antes de "Amazon Gas")
TOTAL = 17.8

a = json.loads((ROOT / "assets/audio/voz-alignment.json").read_text())
words, cur, st, en = [], "", None, None
for ch, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if ch == " ":
        if cur:
            words.append([cur, st + VO, en + VO])
        cur = ""
        continue
    if not cur:
        st = s
    cur += ch
    en = e
if cur:
    words.append([cur, st + VO, en + VO])
VOZ_DUR = round(words[-1][2] - VO, 2)

# Subtítulos: grupos de hasta 3 palabras / 16 caracteres, cortando en puntuación; solo antes del cierre.
groups, g = [], []
for w in words:
    if w[1] >= END - 0.05:
        break
    g.append(w)
    txt = " ".join(x[0] for x in g)
    if w[0][-1] in ".,:?" or len(g) >= 3 or len(txt) >= 16:
        groups.append(g)
        g = []
if g:
    groups.append(g)

caps_html, caps_js = [], []
for i, g in enumerate(groups):
    start = g[0][1]
    nxt = groups[i + 1][0][1] if i + 1 < len(groups) else END
    dur = round(min(nxt, END) - start, 2)
    spans = " ".join(f'<span class="w" id="w{i}_{j}">{w[0]}</span>' for j, w in enumerate(g))
    caps_html.append(f'      <div id="cap{i}" class="clip cap" data-start="{start:.2f}" data-duration="{dur:.2f}" '
                     f'data-track-index="4"><div class="cap-in">{spans}</div></div>')
    caps_js.append(f'      tl.fromTo("#cap{i} .cap-in", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {start:.2f});')
    for j, w in enumerate(g):
        caps_js.append(f'      tl.fromTo("#w{i}_{j}", {{ color: "#fbf8f3" }}, {{ color: "#f5dc17", duration: 0.06 }}, {w[1]:.2f});')


def t(word_idx):
    return round(words[word_idx][1], 2)


# Índices de palabras clave en el guion
I_PERO = [w[0] for w in words].index("Pero")
I_PORQUE = [w[0] for w in words].index("Porque")
I_ES = [w[0] for w in words].index("Es")
T_ES, T_PERO, T_PORQUE = t(I_ES), t(I_PERO), t(I_PORQUE)

# Tomas: [id, src, inicio, duración, media-start]
S1 = (0.0, round(T_ES + 0.35, 2))                 # foto real: convoy navegando al amanecer (gancho)
S2 = (S1[1] - 0.4, round(T_PERO - 0.15 - (S1[1] - 0.4), 2))  # aérea: el cauce entre la selva
S3 = (round(T_PERO - 0.55, 2), round(T_PORQUE - 0.15 - (T_PERO - 0.55), 2))  # barcaza real en la orilla
S4 = (round(T_PORQUE - 0.55, 2), round(END + 0.4 - (T_PORQUE - 0.55), 2))    # vuelve la barcaza navegando
S4_MEDIA = None

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

      :root {{
        --granate: #8e4149;
        --granate-oscuro: #6e2f35;
        --marron: #1b1512;
        --crema: #fbf8f3;
        --arena: #c9bdb0;
        --llama: #f5dc17;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--marron); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; font-family: "Inter", sans-serif; }}

      .shot-wrap {{ position: absolute; inset: 0; overflow: hidden; }}
      video.shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      img.still {{ position: absolute; top: 0; left: 0; height: 100%; width: auto; max-width: none; }}

      #veil {{
        position: absolute; inset: 0;
        background: linear-gradient(180deg, rgba(27,21,18,0.7) 0%, rgba(27,21,18,0.12) 40%, rgba(27,21,18,0.05) 55%, rgba(27,21,18,0.62) 100%);
      }}

      .card {{ position: absolute; left: 80px; right: 160px; top: 290px; }}
      .kicker {{
        display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 700;
        font-size: 44px; letter-spacing: 0.08em; text-transform: uppercase;
        color: var(--crema); background: var(--granate); padding: 8px 22px 6px;
      }}
      .headline {{
        font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        color: var(--crema); font-size: 150px; line-height: 0.9; letter-spacing: -0.01em;
        text-shadow: 0 4px 24px rgba(27,21,18,0.6); margin-top: 18px;
      }}
      .headline.md {{ font-size: 124px; }}
      .headline em {{ font-style: normal; color: var(--llama); }}
      .headline.box {{ display: inline; background: var(--granate); padding: 4px 22px 0; text-shadow: none;
        -webkit-box-decoration-break: clone; box-decoration-break: clone; line-height: 1.08; }}
      .bar {{ display: block; width: 140px; height: 12px; background: var(--granate); margin-top: 26px; }}

      /* Nivel del río: una línea que baja (la vaciante) */
      #nivel {{ position: absolute; left: 80px; top: 900px; width: 260px; }}
      #nivel .ln {{ height: 6px; background: var(--crema); opacity: 0.9; }}
      #nivel .lbl {{ margin-top: 12px; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 34px;
        letter-spacing: 0.08em; text-transform: uppercase; color: var(--crema); text-shadow: 0 2px 12px rgba(27,21,18,0.8); }}

      .cap {{ position: absolute; left: 70px; right: 150px; top: 1180px; }}
      .cap-in {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 84px; line-height: 1.02;
        text-transform: uppercase; color: var(--crema); text-align: left;
        text-shadow: 0 3px 0 rgba(27,21,18,0.9), 0 0 22px rgba(27,21,18,0.85); }}
      .cap-in .w {{ display: inline-block; }}

      #end {{ position: absolute; inset: 0; background: var(--crema); display: flex; flex-direction: column; align-items: center; justify-content: center; }}
      #end-logo {{ width: 360px; height: auto; display: block; }}
      #end-num {{ margin-top: 70px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 120px; line-height: 0.9;
        text-transform: uppercase; color: var(--granate); text-align: center; }}
      #end-tag {{
        margin-top: 10px; font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase;
        font-size: 84px; line-height: 0.95; color: var(--marron); text-align: center; max-width: 860px;
      }}
      #end-tag em {{ font-style: normal; color: var(--granate); }}
      #end-since {{ margin-top: 40px; font-weight: 600; font-size: 40px; color: #6b5d51; letter-spacing: 0.02em; }}
      #end-handle {{
        margin-top: 64px; font-family: "Barlow Condensed", sans-serif; font-weight: 700; font-size: 44px;
        color: var(--crema); background: var(--granate); padding: 10px 28px 8px;
      }}
      #end-rule {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: var(--granate); }}
      #end-wave {{ position: absolute; left: 0; right: 0; top: 0; height: 22px; background: var(--granate); }}
    </style>
  </head>
  <body>
    <!-- Generado por scripts/build.py. Tomas: fotos reales animadas con kie.ai (Kling 2.1). -->
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <div id="s1-vis" class="shot-wrap"><img id="s1" class="clip still" src="assets/img/rio.jpg" alt="" data-start="{S1[0]}" data-duration="{S1[1]}" data-track-index="0" /></div>
      <div id="s2-vis" class="shot-wrap"><video id="s2" class="clip shot" src="assets/clips/v2-meandro.mp4" data-start="{S2[0]:.2f}" data-duration="{S2[1]}" data-track-index="1" muted playsinline></video></div>
      <div id="s3-vis" class="shot-wrap"><video id="s3" class="clip shot" src="assets/clips/v3-barcaza.mp4" data-start="{S3[0]}" data-duration="{S3[1]}" data-track-index="0" muted playsinline></video></div>
      <div id="s4-vis" class="shot-wrap"><img id="s4" class="clip still" src="assets/img/rio.jpg" alt="" data-start="{S4[0]}" data-duration="{S4[1]}" data-track-index="1" /></div>

      <div id="veil" class="clip" data-start="0" data-duration="{END + 0.4}" data-track-index="2"></div>

      <div id="t1" class="clip card" data-start="0.1" data-duration="{round(T_PERO - 0.2 - 0.1, 2)}" data-track-index="3">
        <div class="t1-in">
          <span class="kicker">Vaciante en Loreto</span>
          <div class="headline">El río baja</div>
        </div>
      </div>
      <div id="nivel" class="clip" data-start="0.4" data-duration="{round(T_PERO - 0.2 - 0.4, 2)}" data-track-index="5">
        <div class="ln"></div><div class="lbl">Nivel del río</div>
      </div>
      <div id="t2" class="clip card" data-start="{round(T_PERO, 2)}" data-duration="{round(END - T_PERO, 2)}" data-track-index="3">
        <div class="t2-in">
          <div class="headline md box">El gas sigue <em>llegando</em></div>
          <span class="bar"></span>
        </div>
      </div>

{chr(10).join(caps_html)}

      <div id="end" class="clip" data-start="{END}" data-duration="{round(TOTAL - END, 2)}" data-track-index="6">
        <div id="end-wave"></div>
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-num">Tres embarcaciones</div>
        <div id="end-tag">abasteciendo <em>Loreto</em></div>
        <div id="end-since">Desde el año 2000 · Iquitos</div>
        <div id="end-handle">@amazongasperu</div>
        <div id="end-rule"></div>
      </div>

      <audio id="musica" src="assets/audio/musica.mp3" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="0.5"
        data-automation='{{"version":1,"lanes":[{{"target":"volume","points":[{{"t":0,"v":0}},{{"t":0.5,"v":1}},{{"t":{round(TOTAL - 1.8, 2)},"v":1}},{{"t":{TOTAL},"v":0}}]}}]}}' data-fx-carve="{{&quot;enabled&quot;:true,&quot;sources&quot;:[&quot;voz&quot;],&quot;strength&quot;:0.8}}"></audio>
      <audio id="voz" src="assets/audio/voz.mp3" data-start="{VO}" data-duration="{VOZ_DUR}" data-track-index="10" data-volume="1"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const E = "power3.out";

      // Gancho: el río baja
      tl.fromTo("#t1 .kicker", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, 0.1);
      tl.fromTo("#t1 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, 0.2);
      tl.to("#t1 .t1-in", {{ opacity: 0, duration: 0.2 }}, {round(T_PERO - 0.4, 2)});
      // La línea del nivel baja lentamente
      tl.fromTo("#nivel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.4);
      tl.fromTo("#nivel", {{ y: -60 }}, {{ y: 120, duration: {round(T_PERO - 0.8, 2)}, ease: "sine.inOut" }}, 0.4);
      tl.to("#nivel", {{ opacity: 0, duration: 0.2 }}, {round(T_PERO - 0.4, 2)});

      // Pero el gas sigue llegando
      tl.fromTo("#t2 .headline", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {T_PERO});
      tl.fromTo("#t2 .bar", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.35, ease: E }}, {round(T_PERO + 0.3, 2)});

      // Foto real del convoy (rio.webp, 3455 px de ancho a 1920 de alto): paneo lento, sin IA
      tl.fromTo("#s1", {{ x: -820, scale: 1.0 }}, {{ x: -1020, scale: 1.04, duration: {S1[1]}, ease: "none" }}, 0);
      tl.fromTo("#s4", {{ x: -1500 }}, {{ x: -1950, duration: {S4[1]}, ease: "none" }}, {S4[0]});

      // Fundidos entre tomas
      tl.fromTo("#s2-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S2[0]:.2f});
      tl.fromTo("#s3-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S3[0]});
      tl.fromTo("#s4-vis", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {S4[0]});

      // Cierre
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, ease: "power1.inOut" }}, {END});
      tl.fromTo("#end-logo", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {END + 0.05});
      tl.fromTo("#end-wave", {{ scaleX: 0, transformOrigin: "100% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {END + 0.2});
      tl.fromTo("#end-rule", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.8, ease: E }}, {END + 0.2});
      tl.fromTo("#end-num", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: E }}, {round(words[[w[0] for w in words].index("tres")][1] - 0.05, 2)});
      tl.fromTo("#end-tag", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: E }}, {round(words[[w[0] for w in words].index("abasteciendo")][1] - 0.05, 2)});
      tl.fromTo("#end-since", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(words[-1][2] + 0.2, 2)});
      tl.fromTo("#end-handle", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {round(words[-1][2] + 0.5, 2)});

      // Subtítulos: la palabra que se dice se enciende en amarillo llama
{chr(10).join(caps_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(html)
print("ok", {"S1": S1, "S2": S2, "S3": S3, "S4": S4, "media4": S4_MEDIA, "groups": len(groups), "voz": VOZ_DUR})
