# Country Trend Comparisons

I added a simple reproducible comparison of **1990 and the latest available under-five mortality estimates**, alongside the annualized absolute change from 2015 where both endpoints exist.

This is useful because the **largest percentage improvement** and the **lowest latest mortality rate** are not necessarily the same thing. It also makes the time period behind a comparison explicit.

Run:

```bash
python scripts/05_trend_comparisons.py
```

The script reads `data/clean_countries.csv` and exports `output/country_trend_comparison.csv`. It requires no additional Python packages.

The results cover **only the ten selected countries**. They are historical estimates from the sourced OWID extract, not direct measurement in every year. An annualized change is a descriptive comparison, not a forecast or an estimate of an intervention's effect.
