from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "ticket_prices_raw.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = PROCESSED_DIR / "ticket_prices_clean.csv"


def main():
    df = pd.read_csv(RAW_FILE)

    df["ticket_type"] = df["ticket_type"].astype(str).str.strip()
    df["ticket_tier"] = df["ticket_tier"].astype(str).str.strip().str.upper()
    df["access_level"] = df["access_level"].astype(str).str.strip()

    df["duration_days"] = pd.to_numeric(df["duration_days"], errors="coerce")
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")

    df["price_per_day"] = (df["price_usd"] / df["duration_days"]).round(2)

    df["vip_flag"] = df["ticket_tier"].isin(["VIP", "PLATINUM", "INSIDER"]).astype(int)
    df["premium_flag"] = df["ticket_tier"].isin(["GA+", "VIP", "PLATINUM", "INSIDER"]).astype(int)

    df = df.drop_duplicates(subset=["ticket_type"])

    df = df[
        [
            "ticket_type",
            "ticket_tier",
            "duration_days",
            "access_level",
            "price_usd",
            "price_per_day",
            "vip_flag",
            "premium_flag",
        ]
    ]

    df.to_csv(OUT_FILE, index=False)

    print(f"Saved cleaned ticket prices to: {OUT_FILE}")
    print(f"Rows: {len(df)}")
    print(df)


if __name__ == "__main__":
    main()