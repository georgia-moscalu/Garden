import urllib.request
import json
import threading

PICO_IP = "http://172.21.255.231"

_cache = {"umiditate": 0, "status": "offline", "alarma": False, "temp": 0}

def _background_fetch():
    while True:
        try:
            with urllib.request.urlopen(f"{PICO_IP}/date", timeout=3) as r:
                global _cache
                _cache = json.loads(r.read())
        except:
            pass
        threading.Event().wait(5)  # așteaptă 5 secunde

# Pornește thread-ul de fundal o singură dată la import
threading.Thread(target=_background_fetch, daemon=True).start()

def get_sensor_data() -> dict:
    return _cache  # instant, fără așteptare!

def get_umiditate() -> int:
    return _cache.get("umiditate", 0)