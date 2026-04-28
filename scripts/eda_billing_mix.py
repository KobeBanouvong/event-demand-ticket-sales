import pandas as pd
import matplotlib.pyplot as plt

INPUT_PATH = "data/processed/lineup_with_popularity.csv"

df = pd.read_csv(INPUT_PATH)

billing_mix = (
    df.groupby(["festival_day", "billing_tier"])
      .size()
      .unstack(fill_value=0)
)

day_order = ["Thursday", "Friday", "Saturday", "Sunday"]
tier_order = ["Lower", "Mid", "Upper", "Headliner"]

billing_mix = billing_mix.reindex(day_order)
billing_mix = billing_mix[tier_order]

ax = billing_mix.plot(
    kind="bar",
    stacked=True,
    figsize=(10, 6),
    width=0.7
)

plt.title("Billing Tier Composition by Festival Day", fontsize=16, pad=15)
plt.xlabel("")
plt.ylabel("Artist Count", fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.legend(
    title="Billing Tier",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    frameon=False
)

plt.tight_layout()
plt.savefig("outputs/billing_tier_mix_by_day.png", dpi=300, bbox_inches="tight")
plt.close()

print("Saved billing tier mix chart.")