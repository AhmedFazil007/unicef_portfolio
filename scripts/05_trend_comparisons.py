"""Reproduce country-level trend comparisons using the cleaned OWID extract.
Run: python scripts/05_trend_comparisons.py
No external packages required.
"""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/"data/clean_countries.csv").open(newline="",encoding="utf-8") as f:
    rows=list(csv.DictReader(f))
countries={}
for r in rows:
    countries.setdefault(r["entity"],{})[int(r["year"])]=float(r["u5mr"])
results=[]
for name,series in sorted(countries.items()):
    latest_year=max(series);latest=series[latest_year]
    base=series.get(1990)
    if base is None: continue
    reduction=(base-latest)/base*100 if base else None
    # 2015-to-latest annualized absolute change; not a predictive forecast.
    rate=(latest-series[2015])/(latest_year-2015) if 2015 in series and latest_year>2015 else None
    results.append([name,1990,base,latest_year,latest,round(reduction,2),
                    round(rate,4) if rate is not None else ""])
OUT=ROOT/"output/country_trend_comparison.csv"
with OUT.open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["country","base_year","rate_1990","latest_year","latest_rate",
       "pct_reduction_since_1990","annual_absolute_change_2015_to_latest"])
    w.writerows(results)
print("Wrote",OUT,"for",len(results),"countries")
print("Rates are expressed per 100 live births in the supplied source extract.")
