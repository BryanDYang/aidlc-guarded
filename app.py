"""Utility Co Grid Services — outage and customer service API.

A small Flask service for a fictional California electric utility. Tracks
customers, their meters, and grid outages, with a couple of reporting
endpoints for the operations desk. Uses SQLite for storage and seeds
sample data on first run.

Run:
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python app.py              # listens on PORT env var, default 5060

Then:
    curl http://localhost:5060/customers
    curl http://localhost:5060/outages
    curl http://localhost:5060/reports/outage-summary
"""

import os

from flask import Flask, jsonify

from db import init_db
from seed import seed_if_empty
from api.customers import customers_bp
from api.meters import meters_bp
from api.outages import outages_bp
from api.reports import reports_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(customers_bp)
    app.register_blueprint(meters_bp)
    app.register_blueprint(outages_bp)
    app.register_blueprint(reports_bp)

    @app.route("/")
    def index():
        return jsonify({
            "service": "Utility Co Grid Services outage and customer service API",
            "version": "0.1.0",
            "endpoints": [
                "GET  /customers",
                "POST /customers",
                "GET  /customers/<id>",
                "GET  /customers/<id>/meters",
                "GET  /meters",
                "GET  /meters/<id>",
                "GET  /outages",
                "POST /outages",
                "GET  /outages/<id>",
                "POST /outages/<id>/restore",
                "GET  /reports/outage-summary",
                "GET  /reports/meters-by-type",
            ],
        })

    return app


if __name__ == "__main__":
    init_db()
    seed_if_empty()
    app = create_app()
    port = int(os.environ.get("PORT", 5060))
    app.run(debug=True, port=port)
