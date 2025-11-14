import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = Path(__file__).resolve().parents[1] / "events.db"

def query_db(query, params=()):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/stats", methods=["GET"])
def stats():
    site_id = request.args.get("site_id")
    date = request.args.get("date")  # format: YYYY-MM-DD

    if not site_id:
        return jsonify({"error": "site_id is required"}), 400

    # Base query
    base_query = "SELECT * FROM events WHERE site_id = ?"
    params = [site_id]

    # Add date filter
    if date:
        base_query += " AND timestamp LIKE ?"
        params.append(f"{date}%")

    events = query_db(base_query, params)

    # aggregate
    total_views = len(events)
    unique_users = len(set(row["user_id"] for row in events if row["user_id"]))

    # top paths
    path_counts = {}
    for row in events:
        p = row["path"]
        if p:
            path_counts[p] = path_counts.get(p, 0) + 1

    top_paths = [
        {"path": p, "views": v}
        for p, v in sorted(path_counts.items(), key=lambda x: x[1], reverse=True)
    ]

    response = {
        "site_id": site_id,
        "date": date,
        "total_views": total_views,
        "unique_users": unique_users,
        "top_paths": top_paths,
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port=6000, debug=True)
