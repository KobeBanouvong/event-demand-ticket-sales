import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/lineup_with_popularity.csv"

df = pd.read_csv(INPUT_PATH)

day_order = ["Thursday", "Friday", "Saturday", "Sunday"]
data = [df[df["festival_day"] == day]["artist_popularity_score"] for day in day_order]

plt.figure(figsize=(10, 6))
plt.boxplot(data, tick_labels=day_order)
plt.title("Artist Popularity Distribution by Festival Day")
plt.xlabel("Festival Day")
plt.ylabel("Artist Popularity Score")
plt.tight_layout()
plt.savefig("outputs/popularity_distribution_by_day.png", dpi=300)
plt.close()

print("Saved popularity distribution chart.")