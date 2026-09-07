import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"

countries = pd.read_csv("../data/clean_countries.csv")
regions = pd.read_csv("../data/clean_regions.csv")
latest = pd.read_csv("../output/query_1_latest_ranked.csv")
reduction = pd.read_csv("../output/query_2_pct_reduction_since_1990.csv")
regional_trend = pd.read_csv("../output/query_4_regional_decade_trend.csv")

NAVY = "#12263A"
TEAL = "#2DD4BF"
GOLD = "#B08D3D"

# ---------- Chart 1: Latest under-5 mortality rate by country ----------
fig, ax = plt.subplots(figsize=(8, 5))
latest_sorted = latest.sort_values("latest_u5mr")
ax.barh(latest_sorted["entity"], latest_sorted["latest_u5mr"], color=TEAL, edgecolor=NAVY)
ax.set_xlabel("Under-5 mortality rate (deaths per 100 live births), 2024")
ax.set_title("Under-Five Mortality Rate by Country (Latest Year)", fontsize=13, color=NAVY, weight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("../output/chart_latest_by_country.png", dpi=150)
plt.close()

# ---------- Chart 2: % reduction since 1990 ----------
fig, ax = plt.subplots(figsize=(8, 5))
red_sorted = reduction.sort_values("pct_reduction")
ax.barh(red_sorted["entity"], red_sorted["pct_reduction"], color=GOLD, edgecolor=NAVY)
ax.set_xlabel("% reduction in under-5 mortality, 1990 to 2024")
ax.set_title("Progress Since 1990 by Country", fontsize=13, color=NAVY, weight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("../output/chart_pct_reduction.png", dpi=150)
plt.close()

# ---------- Chart 3: Regional trend lines ----------
fig, ax = plt.subplots(figsize=(8, 5))
years = [1990, 2000, 2010, 2024]
colors = [NAVY, TEAL, GOLD, "#8C8C8C"]
for (idx, row), color in zip(regional_trend.iterrows(), colors):
    values = [row["y1990"], row["y2000"], row["y2010"], row["y2024"]]
    ax.plot(years, values, marker="o", label=row["entity"], color=color, linewidth=2)
ax.set_xlabel("Year")
ax.set_ylabel("Under-5 mortality rate")
ax.set_title("Regional Trends in Under-Five Mortality (1990–2024)", fontsize=13, color=NAVY, weight="bold")
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("../output/chart_regional_trend.png", dpi=150)
plt.close()

# ---------- Chart 4: Full time series per country (line chart) ----------
fig, ax = plt.subplots(figsize=(9, 5.5))
for entity, grp in countries.groupby("entity"):
    ax.plot(grp["year"], grp["u5mr"], label=entity, linewidth=1.6)
ax.set_xlabel("Year")
ax.set_ylabel("Under-5 mortality rate")
ax.set_title("Full Historical Trend by Country", fontsize=13, color=NAVY, weight="bold")
ax.legend(frameon=False, fontsize=8, ncol=2)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("../output/chart_full_timeseries.png", dpi=150)
plt.close()

print("Charts saved to ../output/")
