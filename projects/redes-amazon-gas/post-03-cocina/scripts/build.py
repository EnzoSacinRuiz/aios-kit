"""Genera index.html desde template.html: subtítulos por palabra a partir de la alineación de Terry."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFF = 0.2  # la voz arranca 0.2 s después del inicio
MAXW = 3   # palabras por bloque de subtítulo

al = json.loads((ROOT / "assets/audio/voz-alignment.json").read_text())
chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
text = "".join(chars)
mask = [False] * len(text)
for m in re.finditer(r"<break[^>]*/>", text):
    for i in range(m.start(), m.end()):
        mask[i] = True

words = []
for m in re.finditer(r"\S+", text):
    if any(mask[m.start():m.end()]):
        continue
    words.append((m.group(), st[m.start()] + OFF, en[m.end() - 1] + OFF))

chunks, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    gap = words[i + 1][1] - w[2] if i + 1 < len(words) else 9
    if len(cur) >= MAXW or w[0][-1] in ".?,:" or gap > 0.3:
        chunks.append(cur)
        cur = []
if cur:
    chunks.append(cur)

HIDE = (23.9, 27.65)  # plano del balón: la tarjeta "¡Listo!" ya dice el texto y el subtítulo taparía el balón

html, js = [], []
for c, ws in enumerate(chunks):
    a = ws[0][1]
    if HIDE[0] <= a < HIDE[1]:
        continue
    nxt = chunks[c + 1][0][1] if c + 1 < len(chunks) else ws[-1][2] + 0.3
    b = min(nxt, ws[-1][2] + 0.5)
    spans = " ".join(f'<span class="w" id="w{c}_{k}">{w[0]}</span>' for k, w in enumerate(ws))
    html.append(f'      <div id="cap{c}" class="clip cap" data-start="{a:.2f}" data-duration="{b - a:.2f}" '
                f'data-track-index="4"><div class="cap-in">{spans}</div></div>')
    js.append(f'      tl.fromTo("#cap{c} .cap-in", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {a:.2f});')
    for k, w in enumerate(ws):
        js.append(f'      tl.fromTo("#w{c}_{k}", {{ color: "#fbf8f3" }}, {{ color: "#f5dc17", duration: 0.06 }}, {w[1]:.2f});')

out = (ROOT / "scripts/template.html.tpl").read_text()
out = out.replace("<!--CAPTIONS-->", "\n".join(html)).replace("//CAPTIONS_JS", "\n".join(js))
out = out.replace("__OFF__", str(OFF)).replace("__VOZDUR__", f"{en[-1] + 0.05:.2f}")
(ROOT / "index.html").write_text(out)
print("palabras", len(words), "bloques", len(chunks), "voz termina", round(en[-1] + OFF, 2))
