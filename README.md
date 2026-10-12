# GoldRate Intelligence

**A Python-Based Gold Rate Tracking, Analytics, and Visualization Platform**

GoldRate Intelligence is a Python-based data analytics project that collects published daily gold prices for Chennai, maintains historical records, analyzes price movements, and presents insights through an interactive web dashboard.

The platform combines web scraping, data processing, SQLite storage, REST API development, automated testing, and scheduled execution in a single application.

## Key Features

- **Automated Data Collection:** Scrapes published gold rates using Requests and BeautifulSoup.
- **Historical Data Management:** Stores and maintains gold-price records in SQLite.
- **Data Export:** Supports JSON and CSV data formats.
- **Gold Price Analytics:** Calculates daily price differences and percentage changes for 22K and 24K gold.
- **REST API:** Provides endpoints through FastAPI with interactive Swagger documentation.
- **Interactive Dashboard:** Displays gold prices, historical trends, and records using HTML, CSS, JavaScript, and Chart.js.
- **Scheduled Updates:** Automates daily data collection using Windows Task Scheduler.
- **Automated Testing:** Uses pytest to validate API functionality.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Web Scraping | Requests, BeautifulSoup |
| Backend API | FastAPI, Pydantic |
| Database | SQLite |
| Data Formats | JSON, CSV |
| Frontend | HTML5, CSS3, JavaScript |
| Data Visualization | Chart.js |
| Testing | pytest |
| Automation | Windows Task Scheduler |
| Development Tools | VS Code, Git, GitHub |

## Project Architecture

```text
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
```

## Getting Started

### Prerequisites

- Python installed on your system
- Git
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/yokeshvenkadachalam/GoldRate-Intelligence.git
cd GoldRate-Intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Update the gold-price data

```bash
python daily_update.py
```

This runs the data collection and database update pipeline.

### 5. Start the FastAPI server

```bash
python -m uvicorn main:app --reload
```

Open the API documentation:

http://127.0.0.1:8000/docs

### 6. Open the dashboard

Open `frontend/index.html` with the VS Code Live Server extension while the API server is running.

### 7. Run automated tests

```bash
python -m pytest tests -v
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | API home endpoint |
| `GET /api/gold/latest?city=Chennai` | Retrieves the latest available gold rates |
| `GET /api/gold/history?city=Chennai&limit=10` | Retrieves historical gold-rate records |
| `GET /api/gold/analysis?city=Chennai` | Retrieves price-change analysis |

Interactive testing is available through the FastAPI Swagger interface at `/docs`.

## Data Source

Gold-rate data is collected from LiveChennai:

https://www.livechennai.com/gold_silverrate.asp

The application presents published daily rates rather than live, tick-by-tick market prices. Data availability, accuracy, and update frequency depend on the source website.

## Automation

The daily update pipeline can be scheduled using Windows Task Scheduler. Execution logs help verify whether the scraping and database update process completed successfully.

The computer must be running or otherwise able to execute the scheduled task, with internet access available when the data is collected.

## Future Enhancements

- Deploy the API and dashboard to a public hosting platform.
- Add interactive date-range filtering and additional analytics.
- Introduce data-source health checks and retry mechanisms.
- Set up continuous integration for automated testing.
- Improve dashboard accessibility and mobile usability.

## Disclaimer

This project is intended for educational and informational purposes only. Gold prices may vary across sources, locations, taxes, and jewellers. Verify rates with a reliable source before making financial decisions.

## Author

**Yokesh V**

GitHub: https://github.com/yokeshvenkadachalam

