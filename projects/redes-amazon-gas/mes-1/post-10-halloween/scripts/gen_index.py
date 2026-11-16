"""Genera index.html del post 10 (Doña Meche: Halloween + Día de la Canción Criolla) a partir de
las alineaciones de voz. Copia el patrón del post 4.

Estructura: plano A (cocinando para la jarana) → inserto D (la llama se apaga) → plano B (susto) →
plano C (consejo + CTA) → cierre con balón real y CTA.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUD = ROOT / "assets/audio"


def voice_end(k):
    al = json.loads((AUD / f"voz-{k}-alignment.json").read_text())
    return al["character_end_times_seconds"][-1]


# Tiempos (s). Los planos con diálogo duran lo que la voz + un respiro corto.
A0 = 0.0
A_D = round(voice_end("a") + 0.15, 2)
D0, D_D = A0 + A_D, 2.20
B0 = round(D0 + D_D, 2)
B_D = round(voice_end("b") + 0.35, 2)
C0 = round(B0 + B_D, 2)
C_D = round(voice_end("c") + 0.15, 2)
E0, E_D = round(C0 + C_D, 2), 3.40
TOTAL = round(E0 + E_D, 2)

LINES = {"a": A0, "b": B0, "c": C0}
LINE_END = {"a": A0 + A_D, "b": B0 + B_D, "c": C0 + C_D}
MAXW = 3  # palabras por subtítulo


def words(key):
    al = json.loads((AUD / f"voz-{key}-alignment.json").read_text())
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur, t0, t1 = [], "", None, None
    for c, s, e in zip(chars, st, en):
        if c.isspace():
            if cur:
                out.append((cur, t0, t1)); cur = ""
            continue
        if not cur:
            t0 = s
        cur += c; t1 = e
    if cur:
        out.append((cur, t0, t1))
    return out


def chunks(ws):
    res, cur = [], []
    for w in ws:
        cur.append(w)
        if len(cur) >= MAXW or w[0][-1] in ".,:?!":
            res.append(cur); cur = []
    if cur:
        res.append(cur)
    return res


cap_html, cap_js = [], []
n = 0
for key, off in LINES.items():
    cs = chunks(words(key))
    for i, ch in enumerate(cs):
        start = off + ch[0][1]
        end = min(off + (cs[i + 1][0][1] if i + 1 < len(cs) else ch[-1][2] + 0.25), LINE_END[key])
        spans = " ".join(f'<span class="w" id="w{n}_{j}">{w[0]}</span>' for j, w in enumerate(ch))
        cap_html.append(f'      <div id="cap{n}" class="clip cap" data-start="{start:.2f}" data-duration="{end - start:.2f}" '
                        f'data-track-index="5"><div class="cap-in">{spans}</div></div>')
        cap_js.append(f'      tl.fromTo("#cap{n} .cap-in", {{ opacity: 0, y: 14, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.12, ease: "power2.out" }}, {start:.2f});')
        for j, w in enumerate(ch):
            cap_js.append(f'      tl.fromTo("#w{n}_{j}", {{ color: "#fbf8f3" }}, {{ color: "#f5dc17", duration: 0.06 }}, {off + w[1]:.2f});')
        n += 1

MUSIC_END = 22.35  # la pista de ElevenLabs termina (silencio) a los 22.4 s
M_START = B0 + 0.3
M_DUR = TOTAL - M_START
M2 = max(0.0, MUSIC_END - M_DUR)

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
      img.still-full {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      video.shot {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #veil {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(27,21,18,0.45) 0%, rgba(27,21,18,0) 22%, rgba(27,21,18,0) 55%, rgba(27,21,18,0.55) 100%); }}

      /* Gancho */
      #hook {{ position: absolute; left: 60px; right: 60px; top: 120px; text-align: center; }}
      .hook-in {{ display: inline-block; background: var(--granate); padding: 18px 34px 14px; }}
      .hook-t {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; text-transform: uppercase; color: var(--crema);
        font-size: 78px; line-height: 0.95; letter-spacing: 0.005em; }}
      .hook-t em {{ font-style: normal; color: var(--llama); }}

      /* Rótulo del personaje */
      #name {{ position: absolute; left: 60px; top: 1060px; }}
      .name-k {{ display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 64px; text-transform: uppercase;
        color: var(--marron); background: var(--crema); padding: 6px 20px 2px; }}
      .name-s {{ display: block; width: max-content; margin-top: 8px; font-weight: 600; font-size: 34px; color: var(--crema); background: var(--granate); padding: 6px 16px; }}

      /* Inserto */
      #pff {{ position: absolute; left: 0; right: 0; top: 330px; text-align: center; }}
      .pff-t {{ display: inline-block; font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 150px; color: var(--crema);
        text-shadow: 0 4px 0 rgba(27,21,18,0.9), 0 0 30px rgba(27,21,18,0.8); letter-spacing: 0.04em; }}
      .pff-s {{ display: block; margin-top: 4px; font-weight: 700; font-size: 46px; color: var(--crema); text-shadow: 0 2px 14px rgba(27,21,18,0.9); }}

      /* Subtítulos */
      .cap {{ position: absolute; left: 70px; right: 70px; top: 1330px; text-align: center; }}
      .cap-in {{ font-family: "Barlow Condensed", sans-serif; font-weight: 800; font-size: 92px; line-height: 1.0; text-transform: uppercase; color: var(--crema);
        text-shadow: 0 4px 0 rgba(27,21,18,0.95), 0 0 24px rgba(27,21,18,0.9); }}
      .cap-in .w {{ display: inline-block; }}

      /* Cierre */
      #end {{ position: absolute; inset: 0; background: var(--crema); }}
      #end-balon {{ position: absolute; left: 50%; top: 150px; height: 640px; width: auto; transform: translateX(-50%); }}
      #end-logo {{ position: absolute; left: 50%; top: 830px; width: 220px; height: auto; transform: translateX(-50%); }}
      #end-tag {{ position: absolute; left: 70px; right: 70px; top: 1150px; text-align: center; font-family: "Barlow Condensed", sans-serif; font-weight: 800;
        text-transform: uppercase; font-size: 104px; line-height: 0.93; color: var(--marron); }}
      #end-tag em {{ font-style: normal; color: var(--granate); }}
      #end-wa {{ position: absolute; left: 50%; top: 1430px; transform: translateX(-50%); white-space: nowrap; font-family: "Barlow Condensed", sans-serif;
        font-weight: 700; font-size: 60px; color: var(--crema); background: var(--granate); padding: 12px 34px 8px; }}
      #end-handle {{ position: absolute; left: 0; right: 0; top: 1570px; text-align: center; font-weight: 600; font-size: 38px; color: #6b5d51; }}
      #end-rule {{ position: absolute; left: 0; right: 0; bottom: 0; height: 22px; background: var(--granate); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      <!-- Planos: Doña Meche (kie.ai Nano Banana 2 + Kling AI Avatar con la voz de ElevenLabs) -->
      <div id="va-vis" class="shot-wrap"><video id="va" class="clip shot" src="assets/clips/a.mp4" data-start="{A0}" data-duration="{A_D}" data-track-index="0" muted playsinline></video></div>
      <!-- Inserto: dos fotogramas (llama encendida / apagada) con parpadeo, igual que en el post 4 -->
      <div id="vd-vis" class="clip shot-wrap" data-start="{D0}" data-duration="{D_D}" data-track-index="1">
        <div id="vd" class="shot-wrap"><img class="still-full" src="assets/img/e-hornilla-1080.jpg" alt="" /><img id="vd-on" class="still-full" src="assets/img/d-hornilla-1080.jpg" alt="" /></div>
      </div>
      <div id="vb-vis" class="shot-wrap"><video id="vb" class="clip shot" src="assets/clips/b.mp4" data-start="{B0}" data-duration="{B_D}" data-track-index="0" muted playsinline></video></div>
      <div id="vc-vis" class="shot-wrap"><video id="vc" class="clip shot" src="assets/clips/c.mp4" data-start="{C0}" data-duration="{C_D}" data-track-index="1" muted playsinline></video></div>
      <div id="veil" class="clip" data-start="0" data-duration="{E0}" data-track-index="2"></div>

      <div id="hook" class="clip" data-start="0.05" data-duration="{A_D - 0.25:.2f}" data-track-index="3">
        <div class="hook-in"><div class="hook-t">Sábado de <em>Halloween</em><br />y Canción Criolla</div></div>
      </div>
      <div id="name" class="clip" data-start="1.0" data-duration="3.8" data-track-index="4">
        <span class="name-k">Doña Meche</span>
        <span class="name-s">La vecina · ya la conoces</span>
      </div>
      <div id="pff" class="clip" data-start="{D0 + 0.5:.2f}" data-duration="{D_D - 0.5:.2f}" data-track-index="3">
        <span class="pff-t">PFFF…</span>
        <span class="pff-s">y se apagó la candela…</span>
      </div>

{chr(10).join(cap_html)}

      <div id="end" class="clip" data-start="{E0}" data-duration="{E_D}" data-track-index="6">
        <img id="end-balon" src="assets/img/balon-15kg.png" alt="Balón Amazon Gas" />
        <img id="end-logo" src="assets/img/logo.png" alt="Amazon Gas" />
        <div id="end-tag">Que el sábado no te <em>asuste</em></div>
        <div id="end-wa">Pide al WhatsApp 991 511 401</div>
        <div id="end-handle">@amazongasperu · Iquitos</div>
        <div id="end-rule"></div>
      </div>

      <audio id="voz-a" src="assets/audio/voz-a.mp3" data-start="{A0}" data-duration="{A_D}" data-track-index="10" data-volume="1"></audio>
      <audio id="voz-b" src="assets/audio/voz-b.mp3" data-start="{B0}" data-duration="{B_D}" data-track-index="10" data-volume="1"></audio>
      <audio id="voz-c" src="assets/audio/voz-c.mp3" data-start="{C0}" data-duration="{C_D}" data-track-index="10" data-volume="1"></audio>
      <audio id="sfx-llama" src="assets/audio/sfx-llama.mp3" data-start="{D0 + 0.1:.2f}" data-duration="2.0" data-track-index="11" data-volume="0.9"></audio>
      <audio id="sfx-golpe" src="assets/audio/sfx-golpe.mp3" data-start="{D0 + 0.6:.2f}" data-duration="1.8" data-track-index="12" data-volume="0.55"></audio>
      <!-- Música en dos tramos: se calla en el inserto/susto y vuelve desde el seg. M2 de la pista para que su final coincida con el cierre -->
      <audio id="musica" src="assets/audio/musica.mp3" data-start="0" data-duration="{D0 + 0.3:.2f}" data-track-index="13" data-volume="0.2"
        data-fade-in="0.4" data-fade-out="0.3"></audio>
      <audio id="musica-2" src="assets/audio/musica.mp3" data-start="{M_START:.2f}" data-duration="{M_DUR:.2f}" data-media-start="{M2:.2f}" data-track-index="14" data-volume="0.2"
        data-fade-in="0.9" data-fade-out="0.4"></audio>
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const E = "power3.out";

      tl.fromTo("#hook .hook-in", {{ opacity: 0, y: -40, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.7)" }}, 0.05);
      tl.to("#hook .hook-in", {{ opacity: 0, y: -20, duration: 0.2 }}, {A_D - 0.45:.2f});
      tl.fromTo("#name .name-k", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, 1.0);
      tl.fromTo("#name .name-s", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: E }}, 1.12);
      tl.to("#name", {{ opacity: 0, duration: 0.2 }}, 4.6);

      // Corte seco al inserto; leve empuje de cámara sobre la hornilla
      tl.fromTo("#vd", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {D_D}, ease: "none" }}, {D0});
      // La llama parpadea y se apaga
      tl.set("#vd-on", {{ opacity: 1 }}, {D0});
      tl.to("#vd-on", {{ opacity: 0.35, duration: 0.08 }}, {D0 + 0.15:.2f});
      tl.to("#vd-on", {{ opacity: 1, duration: 0.08 }}, {D0 + 0.25:.2f});
      tl.to("#vd-on", {{ opacity: 0.2, duration: 0.08 }}, {D0 + 0.38:.2f});
      tl.to("#vd-on", {{ opacity: 0.8, duration: 0.06 }}, {D0 + 0.48:.2f});
      tl.to("#vd-on", {{ opacity: 0, duration: 0.15 }}, {D0 + 0.58:.2f});
      tl.fromTo("#pff .pff-t", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {D0 + 0.5:.2f});
      tl.fromTo("#pff .pff-s", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: E }}, {D0 + 0.8:.2f});
      // Zoom dramático en el susto
      tl.fromTo("#vb", {{ scale: 1.0 }}, {{ scale: 1.12, duration: 0.5, ease: "power2.out" }}, {B0});
      tl.fromTo("#vb-vis", {{ x: -14 }}, {{ x: 0, duration: 0.3, ease: "elastic.out(1, 0.3)" }}, {B0});

      // Cierre
      tl.fromTo("#end", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.inOut" }}, {E0});
      tl.fromTo("#end-balon", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.4)" }}, {E0 + 0.1:.2f});
      tl.fromTo("#end-logo", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }}, {E0 + 0.35:.2f});
      tl.fromTo("#end-tag", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: E }}, {E0 + 0.6:.2f});
      tl.fromTo("#end-wa", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: E }}, {E0 + 1.0:.2f});
      tl.fromTo("#end-handle", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {E0 + 1.3:.2f});
      tl.fromTo("#end-rule", {{ scaleX: 0, transformOrigin: "0% 50%" }}, {{ scaleX: 1, duration: 0.7, ease: E }}, {E0 + 0.2:.2f});

      // Subtítulos (alineación de ElevenLabs): la palabra dicha se enciende en amarillo llama
{chr(10).join(cap_js)}

      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(html)
print("ok total", TOTAL, "caps", n)
