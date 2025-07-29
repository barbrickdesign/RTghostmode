from flask import Flask, request, jsonify, send_from_directory
import os, json
from datetime import datetime

app = Flask(__name__)
PAYLOAD_DIR = "ghost_payloads"
LOG_FILE = "logs/ghost_events.log"

@app.route("/payloads/<path:filename>")
def serve_payload(filename):
    return send_from_directory(PAYLOAD_DIR, filename)

@app.route("/log_ghost", methods=["POST"])
def log_ghost():
    try:
        os.makedirs("logs", exist_ok=True)

        raw_data = request.data.decode("utf-8").strip()
        if not raw_data:
            return jsonify({"status": "error", "message": "Empty body"}), 400

        try:
            data = json.loads(raw_data)
        except Exception as e:
            return jsonify({"status": "error", "message": f"JSON decode error: {str(e)}"}), 400

        data["ip"] = request.headers.get("X-Forwarded-For", request.remote_addr)
        data["timestamp"] = datetime.utcnow().isoformat()

        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    os.makedirs(PAYLOAD_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
