import queue
import threading
import requests
from flask import Flask, jsonify, request
from printer_vendor import print_badge
from checkin_store import get_status, mark_pending, mark_result, checked_in

app = Flask(__name__)

attendees = {
    "SOL-2026-0001": {"name": "Amara Njoroge", "role": "General Admission"},
    "SOL-2026-0002": {"name": "Idris Bello", "role": "Speaker"},
    "SOL-2026-0003": {"name": "Wren Castellanos", "role": "VIP"},
}

print_queue = queue.Queue()

@app.route("/")
def dashboard():
    return app.send_static_file("index.html")

@app.route("/attendees")
def get_attendees():
    return jsonify(attendees)

@app.route("/checkin/<attendee_id>")
def checkin(attendee_id):
    attendee = attendees.get(attendee_id)
    if attendee is None:
        return jsonify({"error": "Attendee not found"}), 404

    existing = get_status(attendee_id)
    if existing and existing["status"] == "checked_in":
        return jsonify({"status": "already_checked_in", "attendee": existing["name"]})
    if existing and existing["status"] == "pending":
        return jsonify({"status": "pending", "attendee": existing["name"]})

    force_fail = request.args.get("force_fail") == "1"

    mark_pending(attendee_id, attendee["name"])
    print_queue.put({
        "attendee_id": attendee_id,
        "name": attendee["name"],
        "force_fail": force_fail
    })

    return jsonify({"status": "pending", "attendee": attendee["name"]})

@app.route("/status/<attendee_id>")
def status(attendee_id):
    s = get_status(attendee_id)
    if s is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(s)

@app.route("/webhook/print-complete", methods=["POST"])
def print_complete():
    payload = request.get_json()
    mark_result(payload["attendee_id"], payload["success"])
    print("Webhook: print complete for", payload)
    return jsonify({"status": "ack"})

@app.route("/reset", methods=["POST"])
def reset_demo():
    checked_in.clear()
    return jsonify({"status": "reset"})

def worker():
    while True:
        job = print_queue.get()
        if job.get("force_fail"):
            result = {"success": False, "attendee": job["name"]}
        else:
            result = print_badge(job["name"])
        requests.post("http://localhost:8001/webhook/print-complete", json={
            "attendee_id": job["attendee_id"],
            "success": result["success"]
        })

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    app.run(port=8001)