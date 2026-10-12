
import subprocess
import sys
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "daily_update.log"


def log(message):
    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )
    line = f"[{timestamp}] {message}"

    print(line)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(line + "\n")


def run_script(script_path):
    log(f"Starting {script_path.name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=120
    )

    if result.stdout:
        log(result.stdout.strip())

    if result.stderr:
        log(result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_path.name} failed with exit code "
            f"{result.returncode}"
        )

    log(f"Completed {script_path.name}")


def main():
    try:
        run_script(BASE_DIR / "scraper" / "gold_scraper.py")
        run_script(BASE_DIR / "db_manager.py")

        log("Daily gold-rate update completed successfully.")

    except (RuntimeError, OSError, subprocess.TimeoutExpired) as error:
        log(f"UPDATE FAILED: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
