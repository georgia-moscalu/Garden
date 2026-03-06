import urllib.request
import json

# ── Schimbă cu IP-ul afișat în Thonny când pornești Pico! ──────────────────
PICO_IP = "http://172.21.255.231"
def get_sensor_data() -> dict:
    """Returnează datele live de la Pico. Dacă nu e conectat, returnează offline."""
    try:
        url = f"{PICO_IP}/date"
        with urllib.request.urlopen(url, timeout=3) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[Pico] Offline sau eroare: {e}")
        return {
            "umiditate": 0,
            "status":    "offline",
            "alarma":    False,
            "temp":      0,
        }

def get_umiditate() -> int:
    return get_sensor_data().get("umiditate", 0)