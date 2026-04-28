import pandas as pd

INPUT_PATH = "data/processed/lineup_with_popularity.csv"
OUTPUT_PATH = "data/processed/day_features_with_popularity.csv"

df = pd.read_csv(INPUT_PATH)

day_features = (
    df.groupby(["festival_day", "event_date"])
      .agg(
          artist_count=("artist_name", "count"),
          headliner_count=("headliner_flag", "sum"),
          stage_count=("stage", "nunique"),
          premium_acts=("billing_tier", lambda x: (x == "Headliner").sum()),
          unique_billing_tiers=("billing_tier", "nunique"),
          upper_acts=("billing_tier", lambda x: (x == "Upper").sum()),
          mid_acts=("billing_tier", lambda x: (x == "Mid").sum()),
          lower_acts=("billing_tier", lambda x: (x == "Lower").sum()),
          total_popularity=("artist_popularity_score", "sum"),
          avg_popularity=("artist_popularity_score", "mean"),
      )
      .reset_index()
)

day_features["demand_score"] = (
    day_features["total_popularity"] * 0.6
    + day_features["headliner_count"] * 25
    + day_features["upper_acts"] * 8
)

day_features["avg_popularity"] = day_features["avg_popularity"].round(2)
day_features["demand_score"] = day_features["demand_score"].round(2)

day_features.to_csv(OUTPUT_PATH, index=False)

print(day_features)