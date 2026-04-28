import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/lineup_with_popularity.csv"

df = pd.read_csv(INPUT_PATH)

day_order = ["Thursday", "Friday", "Saturday", "Sunday"]

# Top 5 artist popularity contribution by day
top5 = (
    df.sort_values(["festival_day", "artist_popularity_score"], ascending=[True, False])
      .groupby("festival_day")
      .head(5)
      .groupby("festival_day")["artist_popularity_score"]
      .sum()
      .reindex(day_order)
)

total = (
    df.groupby("festival_day")["artist_popularity_score"]
      .sum()
      .reindex(day_order)
)

top5_share = ((top5 / total) * 100).round(2)

plt.figure(figsize=(10, 6))
plt.bar(top5_share.index, top5_share.values)

for i, value in enumerate(top5_share.values):
    plt.text(i, value, f"{value:.1f}%", ha="center", va="bottom")

plt.title("Top 5 Artist Contribution to Total Popularity by Festival Day")
plt.xlabel("Festival Day")
plt.ylabel("Top 5 Share of Total Popularity (%)")
plt.tight_layout()
plt.savefig("outputs/top5_artist_contribution_by_day.png", dpi=300)
plt.close()

print(top5_share)
print("Saved top artist contribution chart.")