import os
import time
import qrcode
import requests
import random
from pathlib import Path

PAYLOADS_DIR = "ghost_payloads"
QR_DIR = "ghost_qr"
INTERVAL_MINUTES = 2  # ← Change as you like

# Always create QR dir at start
os.makedirs(QR_DIR, exist_ok=True)

def get_public_url():
    try:
        r = requests.get("http://localhost:4040/api/tunnels")
        return r.json()["tunnels"][0]["public_url"]
    except Exception as e:
        print(" Ngrok not connected or unreachable.")
        print(f" Error: {e}")
        return None

def shorten_url(url):
    try:
        r = requests.get("https://is.gd/create.php", params={"format": "simple", "url": url})
        return r.text.strip()
    except:
        return url

def list_payloads():
    return sorted([f for f in os.listdir(PAYLOADS_DIR) if f.endswith(".html")])

def rotate_payload(public_url):
    payloads = list_payloads()
    chosen = random.choice(payloads)
    full_url = f"{public_url}/payloads/{chosen}"
    short_url = shorten_url(full_url)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    qr_path = os.path.join(QR_DIR, f"auto_qr_{timestamp}.png")
    qrcode.make(short_url).save(qr_path)

    print(f" [{timestamp}] New QR for: {chosen}")
    print(f" {short_url}")
    print(f"  Saved to: {qr_path}")

if __name__ == "__main__":
    print(" Starting Ghost Mode QR Rotator...")
    public_url = get_public_url()
    if not public_url:
        exit(1)

    while True:
        rotate_payload(public_url)
        time.sleep(INTERVAL_MINUTES * 60)
