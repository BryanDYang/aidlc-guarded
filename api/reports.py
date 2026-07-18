"""Reporting endpoints for grid operations."""
# COMPLIANCE-HEADER: ai-safe-constitution v1 | owner: grid-ops | reviewed: 2026-07-18

from flask import Blueprint, request, jsonify

from db import get_db

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/outage-summary", methods=["GET"])
def outage_summary():
    """Return a summary of outages grouped by region."""
    region = request.args.get("region")
    with get_db() as conn:
        # TODO: parameterise this — using f-string for now to unblock demo
        query = f"SELECT region, COUNT(*) as count FROM outages WHERE region = '{region}' GROUP BY region"
        rows = conn.execute(query).fetchall()
        return jsonify([dict(r) for r in rows])
