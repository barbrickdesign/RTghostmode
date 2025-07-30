# GHOSTMODE

**Anti-Surveillance QR Payload Jammer**
A weaponized Flask + HTML payload system to confuse, overwhelm, and disrupt using links, qr codes or nfc tags. 

![IMG_7638(1)](https://github.com/user-attachments/assets/96e450c3-4bd2-48a5-a8de-2df7016c057d)

##  Installation

### 1. Clone the repo:

```bash
git clone https://github.com/ekomsSavior/ghostmode.git
cd ghostmode
```

### 2. Install Dependencies

```bash
sudo apt update && sudo apt install -y python3 python3-pip unzip
pip3 install flask requests python-whois qrcode --break-system-packages
```

### 3. Install & Set Up Ngrok

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/
```

### 4. Authenticate Ngrok

```bash
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

---

##  Usage

Launch GhostMode like this:

```bash
cd ghostmode
python3 ghost_cli.py
```

GhostMode will:

* Start the Flask server (`ghost_server.py`)
* Tunnel it through Ngrok
* Let you choose a payload
* Shorten the URL with `is.gd`
* Generate and save a QR code in `ghost_qr/`

---

![IMG_7638(2)](https://github.com/user-attachments/assets/44f8089e-811d-48bf-921c-05c68f0aa424)


##  Payload Descriptions

All payloads are stored in `ghost_payloads/`:

| Filename                | Description                                                                              |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| `noise_bomb.html`       | Visual and auditory overload. Disrupts attention and device focus.                       |
| `sensor_scrambler.html` | Uses ek0ms or user-supplied art to visually confuse.        |
| `identity_mask.html`    | Canvas fingerprint obfuscation and identity spoofing.                                    |
| `identity_reveal.html`  | Baits scanners with transparent metadata logging.                                        |
| `intent_storm.html`     | Fires off deep app-linking Android intents to trigger security prompts or app opens.     |
| `signal_jammer.html`    | High-aggression browser disruptor — locks tabs, spams connections, and overloads the UI. |
| `ghost_flash.html`      | Blinking, flashing canvas to overload visual sensors.                                    |
| `chained_payload.html`  | Combines multiple payloads into a single chained attack.                                 |

---

##  Customizing `sensor_scrambler.html`

If you use the **sensor scrambler**, you can customize the artwork shown in the payload.

1. Replace `your_art.png` inside the `ghost_payloads/` folder.
2. Your image must be:

   * **Named exactly:** `your_art.png`
   * **Dimensions:** `500x500 px`
   * **Format:** PNG only

This image will be embedded in the page to confuse AI vision, scanner overlays, and facial detection tools.

---

##  Adding New Payloads

To add your own HTML payload:

1. Drop it into the `ghost_payloads/` folder.
2. It will auto-load into the menu next time you run `ghost_cli.py`.

---

##  Logging

GhostMode logs all browser interaction data to:

```
logs/ghost_events.log
```

If a payload like `identity_reveal.html` is scanned and activated, any fingerprinting or metadata it collects will show up in that log.

---

##  Advanced Tools

### QR Code Rotator

You can rotate payload QR codes on a timer using:

```bash
python3 ghost_qr_rotator.py
```

This cycles through payloads at a set interval — useful for public installations or protest droppoints.

---

## DISCLAIMER:

Only use on devices and networks you have permission to test on.

---
<img width="500" height="500" alt="Untitled_Artwork" src="https://github.com/user-attachments/assets/03c43859-663e-44d9-a3d3-e18e7398d8f4" />



