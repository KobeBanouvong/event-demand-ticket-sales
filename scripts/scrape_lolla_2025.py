from pathlib import Path
import re
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://www.festivaldust.com/festivals/lollapalooza-2025-chicagoil/set-times"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUT = RAW_DIR / "lineup_raw.csv"

DAY_MAP = {
    "Day 1": ("Thursday", "2025-07-31"),
    "Day 2": ("Friday", "2025-08-01"),
    "Day 3": ("Saturday", "2025-08-02"),
    "Day 4": ("Sunday", "2025-08-03"),
}


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def assign_billing_tiers(df):
    df["billing_tier"] = "Lower"
    df["headliner_flag"] = 0

    for day in df["festival_day"].dropna().unique():
        day_idx = df[df["festival_day"] == day].index

        df.loc[day_idx[:2], "billing_tier"] = "Headliner"
        df.loc[day_idx[:2], "headliner_flag"] = 1

        df.loc[day_idx[2:8], "billing_tier"] = "Upper"
        df.loc[day_idx[8:20], "billing_tier"] = "Mid"

    return df


def scrape_pages_by_day():
    html_by_day = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)

        for day_label in DAY_MAP:
            print(f"Clicking {day_label}...")

            page.get_by_text(day_label, exact=True).click()
            page.wait_for_timeout(3000)

            html = page.content()
            html_by_day[day_label] = html

            html_file = RAW_DIR / f"lolla_2025_{day_label.lower().replace(' ', '_')}.html"
            html_file.write_text(html, encoding="utf-8")

        browser.close()

    return html_by_day


def parse_schedule(html, day_label):
    festival_day, event_date = DAY_MAP[day_label]

    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text("\n")
    lines = [clean_text(line) for line in text.split("\n") if clean_text(line)]

    rows = []
    current_stage = None

    stage_names = {
        "T-Mobile",
        "Perry's",
        "Perrys",
        "Lakeshore",
        "BMI",
        "The Grove",
        "Tito's Handmade Vodka",
        "Bud Light",
        "Toyota Music Den",
        "Kidzapalooza",
    }

    time_range_pattern = re.compile(
        r"^\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)\s?-\s?\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)$"
    )

    single_time_pattern = re.compile(
        r"^\d{1,2}(:\d{2})?\s?(AM|PM|am|pm)$"
    )

    skip_exact = {
        "Day 1", "Day 2", "Day 3", "Day 4",
        "Set Times", "Lineup", "Tickets",
    }

    for i, line in enumerate(lines):
        if line in skip_exact:
            continue

        if line in stage_names:
            current_stage = line
            continue

        if single_time_pattern.match(line):
            continue

        if time_range_pattern.match(line):
            artist = lines[i - 1] if i > 0 else None

            if (
                artist
                and artist not in stage_names
                and artist not in skip_exact
                and not single_time_pattern.match(artist)
                and not time_range_pattern.match(artist)
            ):
                rows.append(
                    {
                        "artist_name": artist.title(),
                        "festival_day": festival_day,
                        "event_date": event_date,
                        "stage": current_stage,
                        "set_time": line,
                        "source_url": URL,
                    }
                )

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    df = df.drop_duplicates(
        subset=["artist_name", "festival_day", "stage", "set_time"]
    )

    return df


def main():
    print("Scraping Lollapalooza 2025 set times by day...")
    html_by_day = scrape_pages_by_day()

    print("Parsing schedules...")

    all_dfs = []

    for day_label, html in html_by_day.items():
        df_day = parse_schedule(html, day_label)

        print(f"{day_label}: {len(df_day)} rows")

        if not df_day.empty:
            all_dfs.append(df_day)

    if not all_dfs:
        print("No rows collected.")
        return

    df = pd.concat(all_dfs, ignore_index=True)
    df = assign_billing_tiers(df)

    df.to_csv(CSV_OUT, index=False)

    print(f"\nSaved CSV to: {CSV_OUT}")
    print(f"Total rows collected: {len(df)}")
    print(df.head(20))


if __name__ == "__main__":
    main()