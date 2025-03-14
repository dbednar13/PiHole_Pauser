from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Pi-hole API Configuration
PIHOLE_URL = ""
PIHOLE_PASSWORD = ""

def get_sid():
    """Authenticate with Pi-hole and get a session ID (SID)."""
    data = {"password": PIHOLE_PASSWORD}
    response = requests.post(f"{PIHOLE_URL}/api/auth", json=data, verify=False)

    if response.status_code != 200:
        return None

    sid = response.json().get("session", {}).get("sid")
    return sid

def toggle_pihole(blocking, duration=None):
    """Enable or disable Pi-hole."""
    sid = get_sid()
    if not sid:
        return {"error": "Auth failed"}, 401

    headers = {
        "Content-Type": "application/json",
        "X-FTL-SID": sid
    }
    data = {"blocking": blocking}

    if duration:
        data["timer"] = duration

    response = requests.post(f"{PIHOLE_URL}/api/dns/blocking", json=data, headers=headers, verify=False)
    return response.json()

@app.route("/disable", methods=["GET"])
def disable_pihole():
    """Disable Pi-hole for a set duration (default 300s)."""
    time = request.args.get("time", 600, type=int)
    response = toggle_pihole(False, time)
    return jsonify(response)

@app.route("/enable", methods=["GET"])
def enable_pihole():
    """Re-enable Pi-hole."""
    response = toggle_pihole(True)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
