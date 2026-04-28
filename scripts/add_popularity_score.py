import pandas as pd

INPUT_PATH = "data/processed/lineup_clean.csv"
OUTPUT_PATH = "data/processed/lineup_with_popularity.csv"

df = pd.read_csv(INPUT_PATH)

# Manual artist popularity proxy.
# Higher score = stronger expected audience demand.
popularity_map = {
    "Olivia Rodrigo": 98,
    "Tyler, The Creator": 96,
    "Sabrina Carpenter": 95,
    "TWICE": 94,
    "Luke Combs": 93,
    "A$AP Rocky": 92,
    "RÜFÜS DU SOL": 90,
    "Korn": 88,
}

# Default popularity score by billing tier
tier_defaults = {
    "Headliner": 85,
    "Upper": 65,
    "Mid": 45,
    "Lower": 25,
}

df["artist_popularity_score"] = df["artist_name"].map(popularity_map)

df["artist_popularity_score"] = df["artist_popularity_score"].fillna(
    df["billing_tier"].map(tier_defaults)
)

df["artist_popularity_score"] = df["artist_popularity_score"].astype(int)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Saved file to: {OUTPUT_PATH}")
print(df[["artist_name", "billing_tier", "artist_popularity_score"]].head(20))