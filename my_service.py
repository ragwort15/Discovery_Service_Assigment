import requests
import threading
import time
import sys
from flask import Flask, jsonify

app = Flask(__name__)

REGISTRY = "http://localhost:5001"
SERVICE_NAME = "my-service"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
ADDRESS = f"http://localhost:{PORT}"

@app.route('/hello')
def hello():
    return jsonify({
        "message": f"Hello from instance at port {PORT}!",
        "instance": ADDRESS,
        "service": SERVICE_NAME
    })

@app.route('/health')
def health():
    return jsonify({"status": "up", "port": PORT})

def register():
    try:
        r = requests.post(f"{REGISTRY}/register", json={
            "service": SERVICE_NAME,
            "address": ADDRESS
        })
        print(f"[Instance:{PORT}] Registered → {r.json()}")
    except Exception as e:
        print(f"[Instance:{PORT}] Registration failed: {e}")

def send_heartbeat():
    while True:
        try:
            requests.post(f"{REGISTRY}/heartbeat", json={
                "service": SERVICE_NAME,
                "address": ADDRESS
            })
            print(f"[Instance:{PORT}] Heartbeat sent")
        except Exception as e:
            print(f"[Instance:{PORT}] Heartbeat failed: {e}")
        time.sleep(10)

if __name__ == "__main__":
    register()
    t = threading.Thread(target=send_heartbeat, daemon=True)
    t.start()
    print(f"[Instance:{PORT}] Service running at {ADDRESS}")
    app.run(port=PORT)