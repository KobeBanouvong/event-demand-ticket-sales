from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LINEUP_FILE = PROJECT_ROOT / "data" / "processed" / "lineup_clean.csv"
PRICES_FILE = PROJECT_ROOT / "data" / "processed" / "ticket_prices_clean.csv"

FINAL_DIR = PROJECT_ROOT / "data" / "final"
FINAL_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = FINAL_DIR / "ticket_sales_model.csv"


DAY_CAPACITY = 115000

TIER_WEIGHTS = {
    "Headliner": 1.00,
    "Upper": 0.70,
    "Mid": 0.40,
    "Lower": 0.18,
}


def main():
    lineup = pd.read_csv(LINEUP_FILE)
    prices = pd.read_csv(PRICES_FILE)

    lineup["tier_weight"] = lineup["billing_tier"].map(TIER_WEIGHTS).fillna(0.18)

    day_demand = (
        lineup.groupby(["festival_day", "event_date"], as_index=False)
        .agg(
            artist_count=("artist_name", "count"),
            headliner_count=("headliner_flag", "sum"),
            lineup_strength=("tier_weight", "sum"),
        )
    )

    max_strength = day_demand["lineup_strength"].max()
    day_demand["demand_score"] = (
        70 + 30 * (day_demand["lineup_strength"] / max_strength)
    ).round(1)

    day_demand["estimated_attendance"] = (
        DAY_CAPACITY * (day_demand["demand_score"] / 100)
    ).round(0).astype(int)

    day_demand["sell_through_pct"] = (
        day_demand["estimated_attendance"] / DAY_CAPACITY
    ).round(4)

    day_demand["sold_out_flag"] = (
        day_demand["sell_through_pct"] >= 0.98
    ).astype(int)

    one_day_prices = prices[prices["duration_days"] == 1].copy()

    model_rows = []

    tier_mix = {
        "GA": 0.82,
        "GA+": 0.10,
        "VIP": 0.07,
        "PLATINUM": 0.01,
    }

    for _, day in day_demand.iterrows():
        for _, ticket in one_day_prices.iterrows():
            ticket_tier = ticket["ticket_tier"]
            mix = tier_mix.get(ticket_tier, 0)

            tickets_sold = int(round(day["estimated_attendance"] * mix))
            gross_revenue = tickets_sold * ticket["price_usd"]

            model_rows.append(
                {
                    "festival_day": day["festival_day"],
                    "event_date": day["event_date"],
                    "ticket_type": ticket["ticket_type"],
                    "ticket_tier": ticket_tier,
                    "access_level": ticket["access_level"],
                    "price_usd": ticket["price_usd"],
                    "price_per_day": ticket["price_per_day"],
                    "tickets_sold": tickets_sold,
                    "estimated_attendance": day["estimated_attendance"],
                    "venue_capacity": DAY_CAPACITY,
                    "sell_through_pct": day["sell_through_pct"],
                    "sold_out_flag": day["sold_out_flag"],
                    "artist_count": day["artist_count"],
                    "headliner_count": day["headliner_count"],
                    "lineup_strength": round(day["lineup_strength"], 2),
                    "demand_score": day["demand_score"],
                    "gross_revenue": gross_revenue,
                    "revenue_per_attendee": round(
                        gross_revenue / day["estimated_attendance"], 2
                    ),
                    "pricing_efficiency": round(
                        day["sell_through_pct"] / ticket["price_per_day"], 6
                    ),
                }
            )

    df = pd.DataFrame(model_rows)

    df.to_csv(OUT_FILE, index=False)

    print(f"Saved ticket sales model to: {OUT_FILE}")
    print(f"Rows: {len(df)}")
    print(df.head(20))


if __name__ == "__main__":
    main()