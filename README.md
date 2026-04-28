# Event Demand & Ticket Sales Analytics

## Overview
This project analyzes how festival lineup construction influences projected day-level ticket demand using artist lineup composition from Lollapalooza 2025. The goal was to evaluate whether lineup volume alone explains expected demand, or whether artist popularity concentration is the stronger driver of projected ticket performance.

Because direct ticket sales and revenue data were not publicly available, this project builds a demand scoring framework using lineup composition and artist popularity proxies to estimate expected day-level demand.

This project was designed as a business analytics case study focused on event strategy, pricing, and revenue optimization.

---

## Business Problem
Live event operators must decide how to allocate artists across festival days to maximize:
- ticket demand
- sell-through
- pricing power
- revenue efficiency

A balanced lineup does not always produce balanced demand. This analysis evaluates whether differences in projected demand are driven by:
- lineup volume
- billing structure
- artist popularity concentration

The objective was to identify which festival day is under-optimized and where lineup allocation creates the largest revenue opportunity.

---

## Dataset
The dataset was built by scraping the 2025 Lollapalooza lineup from public event schedule sources.

Each row in the raw dataset represents one artist performing at the festival and includes:
- artist name
- festival day
- event date
- stage
- set time
- billing tier
- headliner flag

### Processed Dataset
The cleaned lineup dataset contains 194 artist-level records across 4 festival days.

Additional engineered features include:
- artist popularity score (proxy)
- day-level lineup composition
- total popularity by day
- average popularity by day
- demand score

---

## Methodology

### 1. Data Collection
- Scraped Lollapalooza 2025 lineup data
- Cleaned and standardized artist-level lineup fields
- Structured artist-level festival schedule dataset

### 2. Feature Engineering
Artist-level data was aggregated into day-level analytical features:
- artist count
- headliner count
- billing tier composition
- stage coverage
- total popularity
- average popularity

A proxy-based artist popularity score was engineered to estimate relative audience pull.

### 3. Demand Score Modeling
A synthetic day-level demand score was constructed using:
- total artist popularity
- headliner concentration
- upper-tier lineup strength

This demand score was used as a proxy for expected day-level ticket demand.

### 4. Exploratory Analysis
EDA was used to evaluate:
- expected demand by day
- popularity concentration by day
- billing tier composition
- popularity distribution
- top artist contribution

---

## Key Findings

### 1. Lineup Volume Was Balanced Across All Days
Artist count and billing composition were nearly identical across Thursday, Friday, Saturday, and Sunday.

This indicates projected demand differences were not driven by lineup quantity alone.

### 2. Friday Had the Strongest Projected Demand
Friday produced the highest:
- total popularity
- average popularity
- projected demand score

This suggests Friday is the strongest projected revenue day.

### 3. Saturday Underperformed Relative to Other Days
Saturday had comparable lineup depth and billing structure, but the weakest projected demand score.

This indicates Saturday is likely under-optimized from a demand perspective.

### 4. Artist Popularity Was More Important Than Lineup Volume
Projected demand differences were better explained by artist popularity concentration than by artist count or billing balance.

This suggests lineup quality matters more than lineup quantity.

### 5. Saturday’s Weakness Was Driven by Lower Top-Artist Concentration
Saturday had the lowest top-5 artist contribution share of any festival day.

This suggests Saturday’s weaker projected demand is driven by weaker top-of-lineup concentration, not weaker full-lineup depth.

---

## Business Recommendations

### 1. Strengthen Saturday’s Marquee Draw
Reallocate one stronger marquee act to Saturday to improve top-end demand concentration and strengthen sell-through on the weakest projected day.

### 2. Prioritize Top-of-Lineup Demand Concentration
Balanced lineup construction does not guarantee balanced demand. Prioritize stronger top-end artist concentration over evenly distributing talent across all days.

### 3. Use Friday as a Premium Pricing Anchor
Friday demonstrated the strongest projected demand and should be positioned as the primary premium pricing day for:
- single-day passes
- VIP pricing
- premium package upsells

### 4. Position Thursday and Sunday as High-Value Conversion Days
Thursday and Sunday outperformed Saturday despite lower expected primetime positioning. These days may be stronger value-oriented conversion opportunities.

### 5. Incorporate Artist-Level Demand Signals Into Booking Strategy
Future lineup planning should incorporate artist-level demand metrics (streaming, social reach, historical draw) to improve pricing and day-level allocation decisions.

---

## Tools Used
- Python
- Pandas
- Matplotlib
- Git / GitHub

---

## Project Outputs
This project produced:
- cleaned artist-level lineup dataset
- engineered day-level demand model
- exploratory demand analysis
- event strategy recommendations
- portfolio-ready business case study

---

## Next Steps
Future iterations could improve this model by incorporating:
- Spotify monthly listeners
- historical ticket pricing
- secondary market resale data
- social engagement metrics
- artist genre clustering
- external demand indicators (Google Trends, streaming momentum)

This would improve model realism and pricing sensitivity.