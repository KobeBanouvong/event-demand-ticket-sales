import pandas as pd

INPUT_PATH = "data/processed/lineup_with_popularity.csv"
OUTPUT_PATH = "data/processed/top5_share_by_day.csv"

df = pd.read_csv(INPUT_PATH)

# total popularity by day
day_totals = (
    df.groupby("festival_day", as_index=False)["artist_popularity_score"]
      .sum()
      .rename(columns={"artist_popularity_score": "total_popularity"})
)

# top 5 popularity by day
top5 = (
    df.sort_values(["festival_day", "artist_popularity_score"], ascending=[True, False])
      .groupby("festival_day")
      .head(5)
      .groupby("festival_day", as_index=False)["artist_popularity_score"]
      .sum()
      .rename(columns={"artist_popularity_score": "top5_popularity"})
)

# merge and calculate share
out = top5.merge(day_totals, on="festival_day")
out["top5_share_pct"] = (out["top5_popularity"] / out["total_popularity"]) * 100
out = out.sort_values("festival_day")

out.to_csv(OUTPUT_PATH, index=False)
print(out)
print(f"Saved to {OUTPUT_PATH}")