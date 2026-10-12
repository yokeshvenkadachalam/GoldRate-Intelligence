
import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "database" / "gold_rates.db"

app = FastAPI(
    title="GoldRate Intelligence API",
    description="API for Chennai gold prices, historical rates, and price analysis.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null"
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)
def get_connection():
    if not DB_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail="Database not found. Run db_manager.py first."
        )

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    return dict(row) if row else None


@app.get("/")
def home():
    return {
        "message": "Welcome to GoldRate Intelligence API",
        "docs": "/docs",
        "endpoints": [
            "/api/gold/latest",
            "/api/gold/history",
            "/api/gold/analysis"
        ]
    }


@app.get("/api/gold/latest")
def get_latest_gold_rate(city: str = Query(default="Chennai")):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT rate_date, city, currency, rate_24k, rate_22k,
                   source, scraped_at
            FROM gold_rates
            WHERE city = ? COLLATE NOCASE
            ORDER BY rate_date DESC
            LIMIT 1
            """,
            (city,)
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"No gold-rate data found for {city}."
        )

    return {
        "success": True,
        "data": row_to_dict(row)
    }


@app.get("/api/gold/history")
def get_gold_history(
    city: str = Query(default="Chennai"),
    limit: int = Query(default=30, ge=1, le=365)
):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT rate_date, city, currency, rate_24k, rate_22k
            FROM gold_rates
            WHERE city = ? COLLATE NOCASE
            ORDER BY rate_date DESC
            LIMIT ?
            """,
            (city, limit)
        ).fetchall()

    return {
        "success": True,
        "count": len(rows),
        "data": [dict(row) for row in rows]
    }


@app.get("/api/gold/analysis")
def get_gold_analysis(city: str = Query(default="Chennai")):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT rate_date, rate_24k, rate_22k
            FROM gold_rates
            WHERE city = ? COLLATE NOCASE
            ORDER BY rate_date DESC
            LIMIT 2
            """,
            (city,)
        ).fetchall()

    if len(rows) < 2:
        raise HTTPException(
            status_code=404,
            detail="At least two dates of gold-rate data are required."
        )

    latest = rows[0]
    previous = rows[1]

    change_24k = latest["rate_24k"] - previous["rate_24k"]
    change_22k = latest["rate_22k"] - previous["rate_22k"]

    percent_24k = (
        change_24k / previous["rate_24k"] * 100
        if previous["rate_24k"] else None
    )

    percent_22k = (
        change_22k / previous["rate_22k"] * 100
        if previous["rate_22k"] else None
    )

    def movement(change):
        if change > 0:
            return "increased"
        if change < 0:
            return "decreased"
        return "unchanged"

    return {
        "success": True,
        "city": city,
        "latest_date": latest["rate_date"],
        "previous_date": previous["rate_date"],
        "currency": "INR",
        "unit": "gram",
        "24k": {
            "latest_price": latest["rate_24k"],
            "previous_price": previous["rate_24k"],
            "change": round(change_24k, 2),
            "percentage_change": round(percent_24k, 2),
            "movement": movement(change_24k)
        },
        "22k": {
            "latest_price": latest["rate_22k"],
            "previous_price": previous["rate_22k"],
            "change": round(change_22k, 2),
            "percentage_change": round(percent_22k, 2),
            "movement": movement(change_22k)
        }
    }
