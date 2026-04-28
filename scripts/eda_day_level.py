import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/day_features_with_popularity.csv"

df = pd.read_csv(INPUT_PATH)
df["event_date"] = pd.to_datetime(df["event_date"])
df = df.sort_values("event_date")

# -------------------------
# Chart 1: Demand Score by Day
# -------------------------
plt.figure(figsize=(10, 6))
plt.bar(df["festival_day"], df["demand_score"])
for i, value in enumerate(df["demand_score"]):
    plt.text(i, value, f"{value:.1f}", ha="center", va="bottom")
plt.title("Expected Demand Score by Festival Day")
plt.xlabel("Festival Day")
plt.ylabel("Demand Score")
plt.tight_layout()
plt.savefig("outputs/demand_score_by_day.png", dpi=300)
plt.close()

# -------------------------
# Chart 2: Total Popularity by Day
# -------------------------
plt.figure(figsize=(10, 6))
plt.bar(df["festival_day"], df["total_popularity"])
for i, value in enumerate(df["total_popularity"]):
    plt.text(i, value, f"{value:.0f}", ha="center", va="bottom")
plt.title("Total Artist Popularity by Festival Day")
plt.xlabel("Festival Day")
plt.ylabel("Total Popularity Score")
plt.tight_layout()
plt.savefig("outputs/total_popularity_by_day.png", dpi=300)
plt.close()

# -------------------------
# Chart 3: Avg Popularity by Day
# -------------------------
plt.figure(figsize=(10, 6))
plt.bar(df["festival_day"], df["avg_popularity"])
for i, value in enumerate(df["avg_popularity"]):
    plt.text(i, value, f"{value:.2f}", ha="center", va="bottom")
plt.title("Average Artist Popularity by Festival Day")
plt.xlabel("Festival Day")
plt.ylabel("Average Popularity Score")
plt.tight_layout()
plt.savefig("outputs/avg_popularity_by_day.png", dpi=300)
plt.close()

print("Saved EDA charts to outputs/")