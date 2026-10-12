import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "gold_rates.json"
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

DB_FILE = DB_DIR / "gold_rates.db"


def create_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gold_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rate_date TEXT NOT NULL,
                city TEXT NOT NULL,
                currency TEXT NOT NULL,
                rate_24k REAL NOT NULL,
                rate_22k REAL NOT NULL,
                source TEXT,
                scraped_at TEXT,
                UNIQUE(rate_date, city)
            )
        """)

    print("Database and table ready.")


def import_json_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    inserted = 0

    with sqlite3.connect(DB_FILE) as conn:
        for record in records:
            cursor = conn.execute("""
                INSERT OR IGNORE INTO gold_rates (
                    rate_date,
                    city,
                    currency,
                    rate_24k,
                    rate_22k,
                    source,
                    scraped_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                record["date"],
                record["city"],
                record["currency"],
                record["rate_24k"],
                record["rate_22k"],
                record["source"],
                record["scraped_at"]
            ))

            inserted += cursor.rowcount

    print(f"Records in JSON: {len(records)}")
    print(f"New records inserted: {inserted}")
    print(f"Database location: {DB_FILE}")


def show_latest_rates():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("""
            SELECT rate_date, city, rate_24k, rate_22k
            FROM gold_rates
            ORDER BY rate_date DESC
            LIMIT 5
        """).fetchall()

    print("\nLatest stored gold rates:")

    for row in rows:
        print(
            f"Date: {row[0]} | City: {row[1]} | "
            f"24K: Rs.{row[2]:,.2f}/g | "
            f"22K: Rs.{row[3]:,.2f}/g"
        )


if __name__ == "__main__":
    create_table()
    import_json_data()
    show_latest_rates()
