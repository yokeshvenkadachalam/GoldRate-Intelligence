
import csv
import json
import re
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "https://www.livechennai.com/gold_silverrate.asp"

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

def clean_price(value):
    """Convert a price like '15,098' into 15098.0."""
    value = value.replace(",", "").strip()
    return float(value)


def scrape_gold_rates():
    headers = {
        "User-Agent": "GoldRateIntelligence/1.0 (educational project)"
    }

    response = requests.get(
        URL,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    # Find table rows containing a date and four price values.
    for row in soup.find_all("tr"):
        cells = [
            cell.get_text(" ", strip=True)
            for cell in row.find_all(["td", "th"])
        ]

        if len(cells) < 5:
            continue

        date_text = cells[0].strip()

        if not re.fullmatch(
            r"\d{1,2}/[A-Za-z]{3}/\d{4}",
            date_text
        ):
            continue

        try:
            rate_date = datetime.strptime(
                date_text, "%d/%b/%Y"
            ).date().isoformat()

            rate_24k = clean_price(cells[1])
            rate_22k = clean_price(cells[3])

            records.append({
                "date": rate_date,
                "city": "Chennai",
                "currency": "INR",
                "unit": "gram",
                "purity_24k": 24,
                "rate_24k": rate_24k,
                "purity_22k": 22,
                "rate_22k": rate_22k,
                "source": URL,
                "scraped_at": datetime.now().astimezone().isoformat()
            })

        except (ValueError, IndexError):
            continue

    if not records:
        raise RuntimeError(
            "No gold-rate records found. "
            "The page structure may have changed."
        )

    # Remove duplicate dates and sort oldest to newest.
    unique_records = {
        record["date"]: record
        for record in records
    }

    records = sorted(
        unique_records.values(),
        key=lambda item: item["date"]
    )

    return records


def save_json(records):
    output = DATA_DIR / "gold_rates.json"

    with output.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print(f"JSON saved: {output}")


def save_csv(records):
    output = DATA_DIR / "gold_rates.csv"

    with output.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=records[0].keys()
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"CSV saved: {output}")


if __name__ == "__main__":
    try:
        rates = scrape_gold_rates()

        print(f"Records collected: {len(rates)}")
        print("Latest collected record:")
        print(json.dumps(rates[-1], indent=4))

        save_json(rates)
        save_csv(rates)

    except requests.RequestException as error:
        print(f"HTTP/network error: {error}")

    except RuntimeError as error:
        print(f"Scraping error: {error}")
