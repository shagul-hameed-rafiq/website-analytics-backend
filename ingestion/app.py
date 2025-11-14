import sys
from pathlib import Path
# ensure project root (one level up from ingestion/) is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

REQUIRED_FIELDS = {"site_id", "event_type", "timestamp"}

def validate_event(data):
    if not isinstance(data, dict):
        return False, "body must be a JSON object"
    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        return False, f"missing fields: {', '.join(sorted(missing))}"
    try:
        # allow trailing Z by converting to +00:00
        datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    except Exception:
        return False, "timestamp must be ISO 8601 (e.g. 2025-11-12T19:30:01Z)"
    return True, None

@app.route("/event", methods=["POST"])
def event():
    data = request.get_json(silent=True)
    ok, err = validate_event(data)
    if not ok:
        return jsonify({"error": err}), 400

    # push to in-memory queue (non-blocking)
    from event_queue.queue_client import push
    push(data)

    # immediately return success (non-blocking)
    return jsonify({"status": "accepted"}), 202

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
