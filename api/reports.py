"""Reporting endpoints for the operations desk."""

from flask import Blueprint, jsonify

from db import get_db

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/outage-summary", methods=["GET"])
def outage_summary():
    """Outage counts and affected customers broken down by status."""
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT status, COUNT(*) AS count,
                   SUM(customers_affected) AS customers_affected
            FROM outages
            GROUP BY status
            """
        ).fetchall()
        breakdown = {
            r["status"]: {
                "count": r["count"],
                "customers_affected": r["customers_affected"],
            }
            for r in rows
        }
        return jsonify({"by_status": breakdown})


@reports_bp.route("/meters-by-type", methods=["GET"])
def meters_by_type():
    """Active meter counts per meter type."""
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT meter_type, COUNT(*) AS active_count
            FROM meters
            WHERE status = 'active'
            GROUP BY meter_type
            ORDER BY meter_type
            """
        ).fetchall()
        return jsonify([dict(r) for r in rows])
