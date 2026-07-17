"""Seed sample data on first run so the API has something to return."""

from db import get_db

CUSTOMERS = [
    ("Avery Martinez",  "1420 Sycamore Ln",   "Riverdale",   "avery.martinez@example.com",  "residential-tou",  "active",   "2019-04-12"),
    ("Jordan Park",     "88 Bear Creek Rd",   "Lakewood",    "jordan.park@example.com",     "residential-flat", "active",   "2020-08-03"),
    ("Sam Rivera",      "2301 Olive Ave",     "Eastfield",   "sam.rivera@example.com",      "residential-tou",  "active",   "2018-01-29"),
    ("Taylor Brooks",   "975 Foothill Blvd",  "Crestview",   "taylor.brooks@example.com",   "residential-tou",  "past_due", "2021-06-17"),
    ("Casey Nguyen",    "16 Harbor View Dr",  "Bayside",     "casey.nguyen@example.com",    "residential-solar","active",   "2022-03-09"),
    ("Morgan Wells",    "504 Granite Way",    "Riverdale",   "morgan.wells@example.com",    "commercial-sm",    "active",   "2017-11-21"),
    ("Riley Cooper",    "7700 Vineyard Ct",   "Mapleton",    "riley.cooper@example.com",    "residential-flat", "active",   "2023-02-14"),
    ("Drew Patel",      "310 Cannery Row",    "Bayside",     "drew.patel@example.com",      "commercial-lg",    "active",   "2016-09-08"),
    ("Quinn Hayes",     "129 Mariposa St",    "Lakewood",    "quinn.hayes@example.com",     "residential-tou",  "closed",   "2015-05-26"),
    ("Robin Sato",      "4815 Shaw Ave",      "Riverdale",   "robin.sato@example.com",      "residential-solar","active",   "2024-01-30"),
    ("Sage Mitchell",   "62 Pine Flat Rd",    "Crestview",   "sage.mitchell@example.com",   "residential-tou",  "active",   "2020-10-11"),
    ("Hayden Lee",      "2200 McHenry Ave",   "Mapleton",    "hayden.lee@example.com",      "commercial-sm",    "past_due", "2019-07-23"),
]

METERS = [
    (1,  "SPL-100481", "residential", "2019-04-15", "active"),
    (2,  "SPL-100732", "residential", "2020-08-05", "active"),
    (3,  "SPL-100119", "residential", "2018-02-01", "active"),
    (4,  "SPL-101204", "residential", "2021-06-20", "active"),
    (5,  "SPL-101377", "residential", "2022-03-12", "active"),
    (6,  "SPL-200218", "commercial",  "2017-11-25", "active"),
    (7,  "SPL-101593", "residential", "2023-02-16", "active"),
    (8,  "SPL-200455", "commercial",  "2016-09-12", "active"),
    (9,  "SPL-100087", "residential", "2015-06-01", "inactive"),
    (10, "SPL-101801", "residential", "2024-02-02", "active"),
    (11, "SPL-100964", "residential", "2020-10-14", "active"),
    (12, "SPL-200312", "commercial",  "2019-07-28", "active"),
]

OUTAGES = [
    ("Riverdale North",  "equipment failure",   "restored", "2026-05-28T14:22:00Z", "2026-05-28T19:40:00Z", 1240),
    ("Bayside Coastal",  "storm damage",        "restored", "2026-06-01T03:05:00Z", "2026-06-02T11:15:00Z", 3180),
    ("Crestview East",   "vegetation contact",  "active",   "2026-06-09T21:48:00Z", None,                   460),
    ("Mapleton Central", "planned maintenance", "active",   "2026-06-10T08:00:00Z", None,                   75),
]


def seed_if_empty():
    """Populate the DB with sample customers, meters, and outages if empty."""
    with get_db() as conn:
        existing = conn.execute("SELECT COUNT(*) AS c FROM customers").fetchone()
        if existing["c"] > 0:
            return

        conn.executemany(
            """
            INSERT INTO customers
                (name, address, city, email, rate_plan, account_status, enrolled_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            CUSTOMERS,
        )
        conn.executemany(
            """
            INSERT INTO meters
                (customer_id, serial_number, meter_type, install_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            METERS,
        )
        conn.executemany(
            """
            INSERT INTO outages
                (region, cause, status, started_at, restored_at, customers_affected)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            OUTAGES,
        )
