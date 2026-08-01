"""Outage CSV export — DEMO VIOLATION (unapproved library: pandas)."""

import pandas as pd
from flask import Blueprint, Response
from db import get_db

export_bp = Blueprint("export", __name__, url_prefix="/export")


@export_bp.route("/outages.csv", methods=["GET"])
def export_outages_csv():
    """Export all outages as CSV using pandas — VIOLATION: pandas not approved."""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM outages").fetchall()
    df = pd.DataFrame([dict(r) for r in rows])
    return Response(df.to_csv(index=False), mimetype="text/csv")