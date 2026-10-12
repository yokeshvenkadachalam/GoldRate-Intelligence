
import json
import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "data" / "gold_rates.json"
DB_FILE = BASE_DIR / "database" / "gold_rates.db"


def create_database():
    """Create the database and gold_rates table."""
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gold_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate_date TEXT NOT NULL,
                city TEXT NOT NULL,
                currency TEXT,
                unit TEXT,
                purity_24k INTEGER,
                rate_24k REAL,
                purity_22k INTEGER,
                rate_22k REAL,
                source TEXT,
                scraped_at TEXT,
                UNIQUE (rate_date, city)
            )
        """)

    print("Database and table ready.")

def migrate_database():
    """Add missing columns to an existing database safely."""
    new_columns = {
        "currency": "TEXT",
        "unit": "TEXT",
        "purity_24k": "INTEGER",
        "rate_24k": "REAL",
        "purity_22k": "INTEGER",
        "rate_22k": "REAL",
        "source": "TEXT",
        "scraped_at": "TEXT",
    }

    with sqlite3.connect(DB_FILE) as conn:
        existing_columns = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(gold_rates)"
            ).fetchall()
        }

        for column, data_type in new_columns.items():
            if column not in existing_columns:
                conn.execute(
                    f"ALTER TABLE gold_rates ADD COLUMN "
                    f"{column} {data_type}"
                )
                print(f"Added missing column: {column}")

    print("Database migration completed.")



def import_json_to_database():
    """Insert new records and update existing records."""
    if not JSON_FILE.exists():
        print(f"JSON file not found: {JSON_FILE}")
        return

    with JSON_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    inserted = 0
    updated = 0
    unchanged = 0

    with sqlite3.connect(DB_FILE) as conn:
        for record in records:
            cursor = conn.execute("""
                SELECT currency, unit, purity_24k, rate_24k,
                       purity_22k, rate_22k, source, scraped_at
                FROM gold_rates
                WHERE rate_date = ? AND city = ?
            """, (record["date"], record["city"]))

            existing = cursor.fetchone()

            values = (
                record["currency"],
                record["unit"],
                record["purity_24k"],
                record["rate_24k"],
                record["purity_22k"],
                record["rate_22k"],
                record["source"],
                record["scraped_at"],
            )

            if existing is None:
                conn.execute("""
                    INSERT INTO gold_rates (
                        rate_date, city, currency, unit,
                        purity_24k, rate_24k, purity_22k,
                        rate_22k, source, scraped_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(rate_date, city) DO UPDATE SET
                        currency = excluded.currency,
                        unit = excluded.unit,
                        purity_24k = excluded.purity_24k,
                        rate_24k = excluded.rate_24k,
                        purity_22k = excluded.purity_22k,
                        rate_22k = excluded.rate_22k,
                        source = excluded.source,
                        scraped_at = excluded.scraped_at
                """, (
                    record["date"],
                    record["city"],
                    *values
                ))
                inserted += 1

            else:
                old_prices = (existing[2], existing[3],
                              existing[4], existing[5])
                new_prices = (
                    record["purity_24k"],
                    record["rate_24k"],
                    record["purity_22k"],
                    record["rate_22k"],
                )

                if old_prices != new_prices:
                  updated += 1
                else:
                 unchanged += 1

                # UPSERT updates all fields for an existing date/city.
                conn.execute("""
                    INSERT INTO gold_rates (
                        rate_date, city, currency, unit,
                        purity_24k, rate_24k, purity_22k,
                        rate_22k, source, scraped_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(rate_date, city) DO UPDATE SET
                        currency = excluded.currency,
                        unit = excluded.unit,
                        purity_24k = excluded.purity_24k,
                        rate_24k = excluded.rate_24k,
                        purity_22k = excluded.purity_22k,
                        rate_22k = excluded.rate_22k,
                        source = excluded.source,
                        scraped_at = excluded.scraped_at
                """, (
                    record["date"],
                    record["city"],
                    *values
                ))

    print(f"Records in JSON: {len(records)}")
    print(f"New records inserted: {inserted}")
    print(f"Existing records with changed prices: {updated}")
    print(f"Records with no price changes: {unchanged}")
    print(f"Database location: {DB_FILE}")


def display_latest_rates(limit=5):
    """Display the latest stored gold rates."""
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("""
            SELECT rate_date, city, rate_24k, rate_22k
            FROM gold_rates
            ORDER BY rate_date DESC
            LIMIT ?
        """, (limit,)).fetchall()

    print("\nLatest stored gold rates:")

    for row in rows:
        print(
            f"Date: {row[0]} | City: {row[1]} | "
            f"24K: Rs.{row[2]:,.2f}/g | "
            f"22K: Rs.{row[3]:,.2f}/g"
        )


if __name__ == "__main__":
    create_database()
    migrate_database()
    import_json_to_database()
    display_latest_rates()
