"""Helpers mínimos para kie.ai (crear tarea, esperar, subir archivos, créditos).

Reintenta con backoff (30, 60, 120 s) ante 429 o errores de red: otros agentes usan la misma
cuenta en paralelo.
"""
import base64, json, re, time, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIOS = ROOT.parents[2]
env = dict(re.findall(r"^([A-Z_]+)=(.*)$", (AIOS / ".env").read_text(), re.M))
KEY = env["KIE_AI_API_KEY"].strip().strip('"')
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def req(url, data=None, headers=H, timeout=180):
    for wait in (30, 60, 120, None):
        try:
            r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                       headers=headers)
            d = json.loads(urllib.request.urlopen(r, timeout=timeout).read())
            if isinstance(d, dict) and d.get("code") == 429 and wait:
                print("429, espero", wait, flush=True); time.sleep(wait); continue
            return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and wait:
                print("HTTP", e.code, "espero", wait, flush=True); time.sleep(wait); continue
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if wait:
                print("red", e, "espero", wait, flush=True); time.sleep(wait); continue
            raise


def credits():
    try:
        return req("https://api.kie.ai/api/v1/chat/credit").get("data")
    except Exception as e:  # noqa: BLE001
        return f"err {e}"


def upload(path: Path, mime: str):
    b64 = base64.b64encode(path.read_bytes()).decode()
    up = req("https://kieai.redpandaai.co/api/file-base64-upload",
             {"base64Data": f"data:{mime};base64,{b64}", "uploadPath": "amazongas", "fileName": path.name})
    return up["data"].get("downloadUrl") or up["data"]["fileUrl"]


def create(model, inp):
    t = req("https://api.kie.ai/api/v1/jobs/createTask", {"model": model, "input": inp})
    if not t.get("data"):
        raise RuntimeError(f"createTask falló: {t}")
    return t["data"]["taskId"]


def wait_all(tasks: dict, timeout=1800, every=15):
    """tasks: {nombre: taskId}. Devuelve {nombre: {state, urls, credits, fail}}."""
    out, pending = {}, dict(tasks)
    deadline = time.time() + timeout
    while pending and time.time() < deadline:
        time.sleep(every)
        for name, tid in list(pending.items()):
            d = req(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={tid}")["data"]
            if d["state"] == "success":
                urls = json.loads(d["resultJson"])["resultUrls"]
                out[name] = {"taskId": tid, "state": "success", "urls": urls, "credits": d.get("creditsConsumed")}
                print(name, "OK", d.get("creditsConsumed"), flush=True)
                pending.pop(name)
            elif d["state"] == "fail":
                out[name] = {"taskId": tid, "state": "fail", "fail": d.get("failMsg")}
                print(name, "FAIL", d.get("failMsg"), flush=True)
                pending.pop(name)
    for name, tid in pending.items():
        out[name] = {"taskId": tid, "state": "timeout"}
    return out


def download(url, dest: Path):
    urllib.request.urlretrieve(url, dest)
    return dest
