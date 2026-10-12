
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "database" / "gold_rates.db"


def get_price_changes():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("""
            SELECT rate_date, rate_24k, rate_22k
            FROM gold_rates
            WHERE city = 'Chennai'
            ORDER BY rate_date DESC
            LIMIT 2
        """).fetchall()

    if len(rows) < 2:
        print("Not enough historical data to compare prices.")
        return

    latest = rows[0]
    previous = rows[1]

    latest_date, latest_24k, latest_22k = latest
    previous_date, previous_24k, previous_22k = previous

    change_24k = latest_24k - previous_24k
    change_22k = latest_22k - previous_22k

    percent_24k = (change_24k / previous_24k) * 100
    percent_22k = (change_22k / previous_22k) * 100

    print("\n========== GOLD PRICE ANALYSIS ==========")
    print(f"Latest date: {latest_date}")
    print(f"Previous available date: {previous_date}")

    print("\n--- 24K Gold (per gram) ---")
    print(f"Latest price: Rs.{latest_24k:,.2f}")
    print(f"Previous price: Rs.{previous_24k:,.2f}")
    print(f"Price change: Rs.{change_24k:+,.2f}")
    print(f"Percentage change: {percent_24k:+.2f}%")

    print("\n--- 22K Gold (per gram) ---")
    print(f"Latest price: Rs.{latest_22k:,.2f}")
    print(f"Previous price: Rs.{previous_22k:,.2f}")
    print(f"Price change: Rs.{change_22k:+,.2f}")
    print(f"Percentage change: {percent_22k:+.2f}%")

    print("\n--- Market Movement ---")
    if change_24k > 0:
        print("24K gold price increased.")
    elif change_24k < 0:
        print("24K gold price decreased.")
    else:
        print("24K gold price remained unchanged.")


if __name__ == "__main__":
    get_price_changes()
