"""Outage tracking endpoints."""

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify

from db import get_db

outages_bp = Blueprint("outages", __name__, url_prefix="/outages")


@outages_bp.route("", methods=["GET"])
def list_outages():
    """List outages, optionally filtered by status."""
    status = request.args.get("status")
    with get_db() as conn:
        if status:
            rows = conn.execute(
                "SELECT id, region, cause, status, started_at, restored_at, customers_affected "
                "FROM outages WHERE status = ? ORDER BY started_at DESC",
                (status,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, region, cause, status, started_at, restored_at, customers_affected "
                "FROM outages ORDER BY started_at DESC"
            ).fetchall()
        return jsonify([dict(r) for r in rows])


@outages_bp.route("", methods=["POST"])
def create_outage():
    """Open a new outage record."""
    payload = request.get_json(silent=True) or {}
    region = payload.get("region")
    if not region:
        return jsonify({"error": "region is required"}), 400

    started_at = payload.get("started_at") or datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cur = conn.execute(
            """
            INSERT INTO outages
                (region, cause, status, started_at, customers_affected)
            VALUES (?, ?, 'active', ?, ?)
            """,
            (
                region,
                payload.get("cause"),
                started_at,
                int(payload.get("customers_affected", 0)),
            ),
        )
        return jsonify({
            "id": cur.lastrowid,
            "region": region,
            "status": "active",
            "started_at": started_at,
        }), 201


@outages_bp.route("/<int:outage_id>", methods=["GET"])
def get_outage(outage_id):
    """Get a single outage by id."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, region, cause, status, started_at, restored_at, customers_affected "
            "FROM outages WHERE id = ?",
            (outage_id,),
        ).fetchone()
        if not row:
            return jsonify({"error": "outage not found"}), 404
        return jsonify(dict(row))


@outages_bp.route("/<int:outage_id>/restore", methods=["POST"])
def restore_outage(outage_id):
    """Mark an outage as restored."""
    restored_at = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        cur = conn.execute(
            "UPDATE outages SET status = 'restored', restored_at = ? "
            "WHERE id = ? AND status = 'active'",
            (restored_at, outage_id),
        )
        if cur.rowcount == 0:
            return jsonify({"error": "outage not found or already restored"}), 404
        return jsonify({
            "id": outage_id,
            "status": "restored",
            "restored_at": restored_at,
        })
