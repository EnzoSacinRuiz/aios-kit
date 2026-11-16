"""Baja con Apify los posts del último mes y sus comentarios (TikTok @amazongas y Facebook amazongasperu).

Uso: python3 scripts/scrape.py [limites|tiktok|facebook|perfiles]   (sin argumentos: los tres últimos)
Salida: data/<red>-posts.json, data/<red>-comentarios.json, perfiles y historial.json (o $DATA_DIR en Railway)
"""
import datetime, json, os, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get("DATA_DIR") or ROOT / "data")
DATA.mkdir(parents=True, exist_ok=True)


def _token():
    """En Railway viene de la variable de entorno; en local, del .env del AIOS."""
    if os.environ.get("APIFY_API_TOKEN"):
        return os.environ["APIFY_API_TOKEN"].strip().strip('"')
    env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (ROOT.parents[2] / ".env").read_text(), re.M))
    return env["APIFY_API_TOKEN"].strip().strip('"')


TOKEN = _token()
DESDE = os.environ.get("SCRAPE_DESDE") or (datetime.date.today() - datetime.timedelta(days=30)).isoformat()  # último mes
TT = "https://www.tiktok.com/@amazongas"
FB = "https://www.facebook.com/amazongasperu"
IG = "amazongasperu"  # @amazongas es de Brasil, ver knowledge/external


def api(path, data=None):
    r = urllib.request.Request(f"https://api.apify.com/v2/{path}{'&' if '?' in path else '?'}token={TOKEN}",
                               data=json.dumps(data).encode() if data is not None else None,
                               headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=360).read())


def run(actor, inp, nombre):
    """Lanza el actor, espera a que termine y guarda su dataset."""
    r = api(f"acts/{actor.replace('/', '~')}/runs", inp)["data"]
    while r["status"] in ("READY", "RUNNING"):
        time.sleep(10)
        r = api(f"actor-runs/{r['id']}")["data"]
    if r["status"] != "SUCCEEDED":  # si falla, se queda el dataset anterior
        print(nombre, r["status"], "se mantiene el dato anterior", flush=True)
        f = DATA / f"{nombre}.json"
        return json.loads(f.read_text()) if f.exists() else []
    items = api(f"datasets/{r['defaultDatasetId']}/items?clean=true&format=json")
    tmp = DATA / f"{nombre}.json.tmp"
    tmp.write_text(json.dumps(items, ensure_ascii=False, indent=1))
    tmp.replace(DATA / f"{nombre}.json")
    print(nombre, r["status"], len(items), "items", "usd", r.get("usageTotalUsd"), flush=True)
    return items


def limites():
    d = api("users/me/limits")["data"]
    print("uso mes usd", d["current"].get("monthlyUsageUsd"), "limite", d["limits"].get("maxMonthlyUsageUsd"))


def tiktok():
    posts = run("clockworks/tiktok-scraper", {
        "profiles": [TT], "resultsPerPage": 50, "oldestPostDateUnified": DESDE,
        "shouldDownloadVideos": False, "shouldDownloadCovers": False, "profileScrapeSections": ["videos"],
    }, "tiktok-posts")
    urls = [p["webVideoUrl"] for p in posts if p.get("webVideoUrl")]
    if urls:
        run("clockworks/tiktok-comments-scraper", {"postURLs": urls, "commentsPerPost": 200, "maxRepliesPerComment": 20},
            "tiktok-comentarios")


def facebook():
    posts = run("apify/facebook-posts-scraper", {
        "startUrls": [{"url": FB}], "resultsLimit": 50, "onlyPostsNewerThan": DESDE,
    }, "facebook-posts")
    urls = [p["url"] for p in posts if p.get("url")]
    if urls:
        run("apify/facebook-comments-scraper", {
            "startUrls": [{"url": u} for u in urls], "resultsLimit": 200, "includeNestedComments": True,
            "viewOption": "RANKED_UNFILTERED",
        }, "facebook-comentarios")


def perfiles():
    """Seguidores de cada red y una foto del día en historial.json. Las redes no muestran el historial: el crecimiento
    se mide acumulando estas fotos."""
    fb = run("apify/facebook-pages-scraper", {"startUrls": [{"url": FB}]}, "facebook-pagina")
    ig = run("apify/instagram-profile-scraper", {"usernames": [IG]}, "instagram-perfil")
    tt = next((p["authorMeta"] for p in leer("tiktok-posts") if isinstance(p.get("authorMeta"), dict)), None)
    hoy = datetime.date.today().isoformat()
    fotos = []
    if fb and fb[0].get("followers") is not None:
        fotos.append({"red": "facebook", "seguidores": fb[0]["followers"]})
    if ig and ig[0].get("followersCount") is not None:
        fotos.append({"red": "instagram", "seguidores": ig[0]["followersCount"], "posts_totales": ig[0].get("postsCount")})
    if tt and tt.get("fans") is not None:
        fotos.append({"red": "tiktok", "seguidores": tt["fans"], "likes_totales": tt.get("heart"), "posts_totales": tt.get("video")})
    historial = [h for h in leer("historial") if not (h["fecha"] == hoy and h["red"] in {f["red"] for f in fotos})]
    historial += [{"fecha": hoy, **f} for f in fotos]
    (DATA / "historial.json").write_text(json.dumps(sorted(historial, key=lambda h: (h["fecha"], h["red"])), indent=1))
    print("historial", hoy, {f["red"]: f["seguidores"] for f in fotos}, flush=True)


def leer(nombre):
    f = DATA / f"{nombre}.json"
    return json.loads(f.read_text()) if f.exists() else []


if __name__ == "__main__":
    que = sys.argv[1:] or ["tiktok", "facebook", "perfiles"]  # perfiles va al final: usa el autor de tiktok-posts
    for q in que:
        globals()[q]()
