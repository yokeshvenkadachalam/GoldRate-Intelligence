# GoldRate Intelligence

A Python-based gold-rate tracking platform that collects published Chennai gold prices, stores historical records in SQLite, exposes REST APIs using FastAPI, and visualizes price trends through an interactive dashboard.

## Features

- Web scraping with Requests and BeautifulSoup
- JSON and CSV data export
- SQLite storage with duplicate prevention
- Historical 22K and 24K gold-rate tracking
- Daily price difference and percentage analysis
- FastAPI REST API with Swagger documentation
- Interactive dashboard built with HTML, CSS, JavaScript, and Chart.js
- Automated update script with execution logs
- Automated API tests using pytest

## Technology Stack

Python, Requests, BeautifulSoup, SQLite, FastAPI, Pydantic, HTML5, CSS3, JavaScript, Chart.js, pytest.

## Project Structure


GoldRate-Intelligence/
├── scraper/
│   └── gold_scraper.py
├── database/
├── data/
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── tests/
│   └── test_api.py
├── main.py
├── db_manager.py
├── price_analysis.py
├── daily_update.py
├── requirements.txt
├── .gitignore
└── README.md


## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Run the data update script:

   `python daily_update.py`

5. Start the API:

   `python -m uvicorn main:app --reload`

6. Open the API documentation at `http://127.0.0.1:8000/docs`.

7. Open `frontend/index.html` with VS Code Live Server to view the dashboard.

## Run Tests

`python -m pytest tests -v`

## Data Source

Daily published Chennai gold-rate data is collected from LiveChennai:
https://www.livechennai.com/gold_silverrate.asp

Data availability, accuracy, and update frequency depend on the source. The project presents published daily rates, not tick-by-tick market prices.

## Future Improvements

- Historical price charts and additional analytics
- Scheduled data collection
- Improved validation and error handling
- Deployment and monitoring
- Additional automated tests

## Disclaimer

This project is for educational and informational purposes. Verify rates with an authoritative source before making financial decisions.
