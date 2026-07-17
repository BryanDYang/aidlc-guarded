"""Customer account endpoints."""

from flask import Blueprint, request, jsonify

from db import get_db

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["GET"])
def list_customers():
    """List customers, optionally filtered by account status."""
    account_status = request.args.get("status")
    with get_db() as conn:
        if account_status:
            rows = conn.execute(
                "SELECT id, name, address, city, email, rate_plan, account_status, enrolled_date "
                "FROM customers WHERE account_status = ? ORDER BY name",
                (account_status,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, name, address, city, email, rate_plan, account_status, enrolled_date "
                "FROM customers ORDER BY name"
            ).fetchall()
        return jsonify([dict(r) for r in rows])


@customers_bp.route("", methods=["POST"])
def create_customer():
    """Enroll a new customer account."""
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    address = payload.get("address")
    city = payload.get("city")
    email = payload.get("email")
    if not name or not address or not city or not email:
        return jsonify({"error": "name, address, city, and email are required"}), 400

    with get_db() as conn:
        try:
            cur = conn.execute(
                """
                INSERT INTO customers
                    (name, address, city, email, rate_plan, account_status, enrolled_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    address,
                    city,
                    email,
                    payload.get("rate_plan", "residential-tou"),
                    payload.get("account_status", "active"),
                    payload.get("enrolled_date", ""),
                ),
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({
            "id": cur.lastrowid,
            "name": name,
            "city": city,
            "email": email,
        }), 201


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """Get a single customer account by id."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, name, address, city, email, rate_plan, account_status, enrolled_date "
            "FROM customers WHERE id = ?",
            (customer_id,),
        ).fetchone()
        if not row:
            return jsonify({"error": "customer not found"}), 404
        return jsonify(dict(row))


@customers_bp.route("/<int:customer_id>/meters", methods=["GET"])
def customer_meters(customer_id):
    """List meters installed for a given customer."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, serial_number, meter_type, install_date, status "
            "FROM meters WHERE customer_id = ? ORDER BY install_date",
            (customer_id,),
        ).fetchall()
        return jsonify([dict(r) for r in rows])
