from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "lineup_raw.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = PROCESSED_DIR / "lineup_clean.csv"


def clean_artist_name(name):
    if pd.isna(name):
        return name

    name = str(name).strip()

    replacements = {
        "Can'T": "Can't",
        "Dj ": "DJ ",
        "B2B": "b2b",
        "A$Ap": "A$AP",
        "Rüfüs": "RÜFÜS",
        "Twice": "TWICE",
        "Djo": "DJO",
        "Bmi": "BMI",
    }

    name = name.title()

    for old, new in replacements.items():
        name = name.replace(old, new)

    return name


def clean_stage(stage):
    if pd.isna(stage):
        return stage

    stage = str(stage).strip()

    stage_map = {
        "Perrys": "Perry's",
        "Perry'S": "Perry's",
        "T-Mobile": "T-Mobile",
        "Bmi": "BMI",
        "Tito'S Handmade Vodka": "Tito's Handmade Vodka",
    }

    stage = stage.title()

    return stage_map.get(stage, stage)


def assign_billing_tiers(df):
    df = df.copy()
    df["billing_tier"] = "Lower"
    df["headliner_flag"] = 0

    # Later set times usually indicate higher billing.
    # This sorts each day from latest to earliest before assigning tier.
    df["_sort_time"] = pd.to_datetime(
        df["set_time"].str.extract(r"-\s?(.+)$")[0],
        format="mixed",
        errors="coerce",
    )

    df = df.sort_values(
        by=["event_date", "_sort_time"],
        ascending=[True, False],
    )

    for day in df["festival_day"].unique():
        idx = df[df["festival_day"] == day].index

        df.loc[idx[:2], "billing_tier"] = "Headliner"
        df.loc[idx[:2], "headliner_flag"] = 1

        df.loc[idx[2:8], "billing_tier"] = "Upper"
        df.loc[idx[8:20], "billing_tier"] = "Mid"

    df = df.drop(columns=["_sort_time"])

    return df


def main():
    df = pd.read_csv(RAW_FILE)

    df["artist_name"] = df["artist_name"].apply(clean_artist_name)
    df["stage"] = df["stage"].apply(clean_stage)

    df["event_date"] = pd.to_datetime(df["event_date"]).dt.date

    df = df.drop_duplicates(
        subset=["artist_name", "festival_day", "event_date", "stage", "set_time"]
    )

    df = assign_billing_tiers(df)

    df = df[
        [
            "artist_name",
            "festival_day",
            "event_date",
            "stage",
            "set_time",
            "billing_tier",
            "headliner_flag",
            "source_url",
        ]
    ]

    df.to_csv(OUT_FILE, index=False)

    print(f"Saved cleaned lineup to: {OUT_FILE}")
    print(f"Rows: {len(df)}")
    print(df.head(20))


if __name__ == "__main__":
    main()