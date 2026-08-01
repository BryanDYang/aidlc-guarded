"""Notify external alerting service — DEMO VIOLATION (inline secret)."""

import requests
from flask import Blueprint

notify_bp = Blueprint("notify", __name__, url_prefix="/notify")

# VIOLATION: API key is hardcoded — should be os.environ.get("ALERT_API_KEY")
ALERT_API_KEY = "DEMO-FAKE-KEY-NOT-REAL-abc123"


@notify_bp.route("/outage/<int:outage_id>", methods=["POST"])
def notify_outage(outage_id):
    """Send outage notification to external alerting service."""
    resp = requests.post(
        "https://alerts.example.com/api/v1/notify",
        headers={"Authorization": f"Bearer {ALERT_API_KEY}"},
        json={"outage_id": outage_id},
    )
    return {"status": resp.status_code}