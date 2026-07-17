"""Meter endpoints."""

from flask import Blueprint, request, jsonify

from db import get_db

meters_bp = Blueprint("meters", __name__, url_prefix="/meters")


@meters_bp.route("", methods=["GET"])
def list_meters():
    """List meters, optionally filtered by status."""
    status = request.args.get("status")
    with get_db() as conn:
        if status:
            rows = conn.execute(
                "SELECT id, customer_id, serial_number, meter_type, install_date, status "
                "FROM meters WHERE status = ? ORDER BY serial_number",
                (status,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, customer_id, serial_number, meter_type, install_date, status "
                "FROM meters ORDER BY serial_number"
            ).fetchall()
        return jsonify([dict(r) for r in rows])


@meters_bp.route("/<int:meter_id>", methods=["GET"])
def get_meter(meter_id):
    """Get a single meter by id."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, customer_id, serial_number, meter_type, install_date, status "
            "FROM meters WHERE id = ?",
            (meter_id,),
        ).fetchone()
        if not row:
            return jsonify({"error": "meter not found"}), 404
        return jsonify(dict(row))
