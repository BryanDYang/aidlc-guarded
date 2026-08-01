"""Reporting endpoints for the operations desk."""

from flask import Blueprint, jsonify, request

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


# ---------------------------------------------------------------------------
# Function: customers_by_city
# Owner:    grid-platform-team
# Control:  AC-3, SI-10   (NERC CIP: CIP-007 R5, CIP-011 R1)
# Reviewed: 2026-07-31
# ---------------------------------------------------------------------------
@reports_bp.route("/customers-by-city", methods=["GET"])
def customers_by_city():
    """Return customers in a validated city for the intentional FAIL demo."""
    city = request.args.get("city", "").strip()
    if not city or len(city) > 80:
        return jsonify({"error": "city must contain 1–80 characters"}), 400

    with get_db() as conn:
        # INTENTIONAL DEMO VIOLATION: user input is interpolated into SQL.
        rows = conn.execute(
            f"SELECT id, name, city FROM customers WHERE city = '{city}' "
            "ORDER BY name"
        ).fetchall()
        return jsonify([dict(row) for row in rows])
