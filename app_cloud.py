"""
app_cloud.py — GOOGLE CLOUD VERSION
Hosting  : Cloud Run (serverless container)
Database : Firestore (NoSQL, serverless)
Messaging: Cloud Pub/Sub (loose coupling for future integrations)
Run      : Deployed via Cloud Run (see README)
"""

import os
import json
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, session

# Google Cloud libraries
from google.cloud import firestore
from google.cloud import pubsub_v1

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cloud-secret-key-change-in-prod")

ADMIN_PASSWORD = "1234"
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
PUBSUB_TOPIC   = os.environ.get("PUBSUB_TOPIC", "event-registrations")

# Initialise Firestore client
db = firestore.Client(project=GCP_PROJECT_ID)

# Initialise Pub/Sub publisher
publisher    = pubsub_v1.PublisherClient()
topic_path   = publisher.topic_path(GCP_PROJECT_ID, PUBSUB_TOPIC)


# ── HELPERS ──────────────────────────────────────────────────────────────────

def publish_registration(data: dict):
    """Publish registration event to Pub/Sub for loose coupling."""
    try:
        message_bytes = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data=message_bytes)
        future.result()  # wait for confirmation
    except Exception as e:
        # Pub/Sub failure should not break registration
        app.logger.warning(f"Pub/Sub publish failed: {e}")


# ── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    full_name  = request.form.get("full_name", "").strip()
    email      = request.form.get("email", "").strip()
    student_id = request.form.get("student_id", "").strip()
    event_name = request.form.get("event_name", "").strip()
    phone      = request.form.get("phone", "").strip()

    if not all([full_name, email, student_id, event_name]):
        flash("All required fields must be filled.", "error")
        return redirect(url_for("index"))

    registered_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Save to Firestore
    doc_ref = db.collection("registrations").document()
    reg_data = {
        "full_name":     full_name,
        "email":         email,
        "student_id":    student_id,
        "event_name":    event_name,
        "phone":         phone or None,
        "registered_at": registered_at,
    }
    doc_ref.set(reg_data)

    # Publish to Pub/Sub (async, non-blocking to UX)
    publish_registration({**reg_data, "doc_id": doc_ref.id})

    flash(f"🎉 You're registered for {event_name}!", "success")
    return redirect(url_for("index"))


# ── ADMIN ─────────────────────────────────────────────────────────────────────

@app.route("/admin")
def admin():
    registrations = []
    if session.get("admin"):
        docs = db.collection("registrations") \
                 .order_by("registered_at", direction=firestore.Query.DESCENDING) \
                 .stream()
        registrations = [{"id": d.id, **d.to_dict()} for d in docs]
    return render_template("admin.html", registrations=registrations)


@app.route("/admin/login", methods=["POST"])
def admin_login():
    password = request.form.get("password", "")
    if password == ADMIN_PASSWORD:
        session["admin"] = True
        return redirect(url_for("admin"))
    flash("Incorrect password.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin"))


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
