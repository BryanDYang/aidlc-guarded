"""Customer delete endpoint — DEMO VIOLATION (hard delete of regulated record)."""

from flask import Blueprint, jsonify
from db import get_db

delete_bp = Blueprint("delete_customer", __name__, url_prefix="/admin")


@delete_bp.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """
    Permanently remove a customer record.
    VIOLATION: hard DELETE on regulated customer data — must be a soft-delete.
    CIP-011 requires regulated records to be retained, not destroyed.
    """
    with get_db() as conn:
        conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    return jsonify({"deleted": customer_id}), 200