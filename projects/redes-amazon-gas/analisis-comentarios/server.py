"""Dashboard en vivo de los comentarios de Amazon Gas (Facebook y TikTok).

Sirve dashboard/index.html y /api/data, y cada SCRAPE_HOURS horas corre scripts/scrape.py en segundo plano.
Uso local: python3 server.py  →  http://localhost:8000
Variables: DASHBOARD_PASSWORD (obligatoria en Railway), DATA_DIR, SCRAPE_HOURS (12), APIFY_API_TOKEN, PORT.
"""
import base64, datetime, hmac, json, os, re, shutil, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = ROOT / "data"
DATA = Path(os.environ.get("DATA_DIR") or SEED)
DATA.mkdir(parents=True, exist_ok=True)
ESTADO = DATA / "estado.json"
HORAS = float(os.environ.get("SCRAPE_HOURS") or 12)
PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "")
EN_RAILWAY = bool(os.environ.get("RAILWAY_ENVIRONMENT"))
META_SEMANA = int(os.environ.get("META_POSTS_SEMANA") or 2)  # la meta vive en context/priorities.md; si cambia, cambia esta variable

# Orden importa: el primer tema que coincide gana ("no llega ni a los 10 kilos" es peso, no precio).
TEMAS = [
    ("peso", "Peso o rendimiento", r"incomplet|mitad|kilo|\bkg\b|peso|pesa|dura|complet|rinde|no llena"),
    ("precio", "Precio", r"car[oa]s?\b|precio|costo|cuesta|abus|margen|barat|ricos|cobran|utilidad|elevad"),
    ("positivo", "Positivo", r"excelente|buen[oa]?\b|gracias|felicit|genial|bravo|recomiend|👍|❤|👏"),
    ("consulta", "Consulta", r"\?|cu[aá]nto|d[oó]nde|delivery|reparto|n[uú]mero|whatsapp|horario"),
]


def tema(texto):
    t = (texto or "").lower()
    for clave, _, patron in TEMAS:
        if re.search(patron, t):
            return clave
    return "otro"


def n(x):
    try:
        return int(x or 0)
    except (TypeError, ValueError):
        return 0


def leer(nombre):
    f = DATA / f"{nombre}.json"
    try:
        return json.loads(f.read_text())
    except (OSError, ValueError):
        return []


def abreviar(nombre):
    partes = (nombre or "").split()
    if not partes:
        return "Anónimo"
    return partes[0] + (f" {partes[1][0]}." if len(partes) > 1 else "")


def datos():
    posts, comentarios = [], []
    for p in leer("facebook-posts"):
        if not p.get("url") or p.get("error") or not p.get("text"):  # sin texto = cambio de foto de perfil o portada
            continue
        posts.append({"red": "facebook", "url": p["url"], "fecha": p.get("time"), "texto": (p.get("text") or "")[:140],
                      "vistas": n(p.get("viewsCount")), "likes": n(p.get("likes")),
                      "comentarios": n(p.get("comments")), "compartidos": n(p.get("shares"))})
    for p in leer("tiktok-posts"):
        if not p.get("webVideoUrl"):
            continue
        posts.append({"red": "tiktok", "url": p["webVideoUrl"], "fecha": p.get("createTimeISO"),
                      "texto": (p.get("text") or "")[:140], "vistas": n(p.get("playCount")), "likes": n(p.get("diggCount")),
                      "comentarios": n(p.get("commentCount")), "compartidos": n(p.get("shareCount"))})
    for c in leer("facebook-comentarios"):
        if not c.get("text"):
            continue
        comentarios.append({"red": "facebook", "fecha": c.get("date"), "texto": c["text"], "tema": tema(c["text"]),
                            "autor": abreviar(c.get("profileName")), "likes": n(c.get("likesCount")),
                            "url": c.get("commentUrl") or c.get("facebookUrl"), "post": (c.get("postTitle") or "")[:80]})
    for c in leer("tiktok-comentarios"):
        if not c.get("text"):
            continue
        comentarios.append({"red": "tiktok", "fecha": c.get("createTimeISO"), "texto": c["text"], "tema": tema(c["text"]),
                            "autor": "Usuario de TikTok", "likes": n(c.get("diggCount")), "url": c.get("videoWebUrl"),
                            "post": ""})
    desde = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    for perfil in leer("instagram-perfil")[:1]:
        for p in perfil.get("latestPosts") or []:
            if not p.get("url") or (p.get("timestamp") or "") < desde:
                continue
            posts.append({"red": "instagram", "url": p["url"], "fecha": p.get("timestamp"),
                          "texto": (p.get("caption") or "")[:140],
                          "vistas": n(p.get("videoPlayCount") or p.get("videoViewCount")), "likes": n(p.get("likesCount")),
                          "comentarios": n(p.get("commentsCount")), "compartidos": 0})
    comentarios.sort(key=lambda c: c["fecha"] or "", reverse=True)
    posts.sort(key=lambda p: p["fecha"] or "", reverse=True)
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    return {"posts": posts, "comentarios": comentarios, "estado": estado, "historial": leer("historial"),
            "meta_semana": META_SEMANA,
            "temas": [{"clave": k, "nombre": nom} for k, nom, _ in TEMAS] + [{"clave": "otro", "nombre": "Otro"}]}


def sembrar():
    """Primer arranque en Railway: el volumen viene vacío, se copia el último scrapeo subido con el código."""
    if DATA == SEED or any(DATA.glob("*-posts.json")):
        return
    for f in SEED.glob("*.json"):
        shutil.copy(f, DATA / f.name)
    print("volumen sembrado con", SEED, flush=True)


def scrapear():
    inicio = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "scrape.py")], capture_output=True, text=True,
                       env={**os.environ, "DATA_DIR": str(DATA)}, timeout=3600)
    estado = {"ultima": inicio, "ok": r.returncode == 0, "log": (r.stdout + r.stderr)[-2000:]}
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=1))
    print("scrape", "ok" if estado["ok"] else "FALLÓ", estado["log"], flush=True)


def programador():
    while True:
        try:
            ultima = json.loads(ESTADO.read_text()).get("ultima") if ESTADO.exists() else None
            vencido = not ultima or not (DATA / "historial.json").exists() or (datetime.datetime.now(datetime.timezone.utc)
                                     - datetime.datetime.fromisoformat(ultima)).total_seconds() > HORAS * 3600
            if vencido:
                scrapear()
        except Exception as e:  # el servidor sigue aunque falle un scrapeo
            print("programador:", e, flush=True)
        time.sleep(600)


class Handler(BaseHTTPRequestHandler):
    def autorizado(self):
        if not PASSWORD:
            return not EN_RAILWAY  # en Railway sin contraseña no se sirve nada
        h = self.headers.get("Authorization", "")
        if not h.startswith("Basic "):
            return False
        try:
            _, _, clave = base64.b64decode(h[6:]).decode().partition(":")
        except ValueError:
            return False
        return hmac.compare_digest(clave, PASSWORD)

    def enviar(self, codigo, cuerpo, tipo):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Robots-Tag", "noindex")
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self):
        if self.path == "/salud":
            return self.enviar(200, b"ok", "text/plain")
        if not self.autorizado():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Amazon Gas"')
            self.end_headers()
            return
        if self.path == "/api/data":
            return self.enviar(200, json.dumps(datos(), ensure_ascii=False).encode(), "application/json")
        if self.path in ("/", "/index.html"):
            return self.enviar(200, (ROOT / "dashboard" / "index.html").read_bytes(), "text/html; charset=utf-8")
        self.enviar(404, b"no encontrado", "text/plain")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    sembrar()
    if EN_RAILWAY or os.environ.get("SCRAPE_LOCAL"):
        threading.Thread(target=programador, daemon=True).start()
    port = int(os.environ.get("PORT") or 8000)
    print(f"dashboard en :{port}, scrapeo cada {HORAS} h, datos en {DATA}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
