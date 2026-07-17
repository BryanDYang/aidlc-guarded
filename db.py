"""SQLite connection helper and schema initialization."""

import sqlite3

DB_PATH = "utility.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS customers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT    NOT NULL,
                address         TEXT    NOT NULL,
                city            TEXT    NOT NULL,
                email           TEXT    NOT NULL UNIQUE,
                rate_plan       TEXT    NOT NULL DEFAULT 'residential-tou',
                account_status  TEXT    NOT NULL DEFAULT 'active',
                enrolled_date   TEXT    NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meters (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id   INTEGER NOT NULL,
                serial_number TEXT    NOT NULL UNIQUE,
                meter_type    TEXT    NOT NULL DEFAULT 'residential',
                install_date  TEXT    NOT NULL,
                status        TEXT    NOT NULL DEFAULT 'active',
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS outages (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                region              TEXT    NOT NULL,
                cause               TEXT,
                status              TEXT    NOT NULL DEFAULT 'active',
                started_at          TEXT    NOT NULL,
                restored_at         TEXT,
                customers_affected  INTEGER NOT NULL DEFAULT 0
            )
            """
        )
