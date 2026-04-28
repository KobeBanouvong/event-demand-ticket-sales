import pandas as pd

df = pd.read_csv("data/processed/lineup_clean.csv")

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
      )
      .reset_index()
    )

day_features["demand_score"] = (
    day_features["headliner_count"] * 40
    + day_features["upper_acts"] * 15
    + day_features["mid_acts"] * 6
    + day_features["lower_acts"] * 2
    + day_features["stage_count"] * 3
)

print(day_features)
day_features.to_csv("data/processed/day_features.csv", index=False)