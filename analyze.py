# analyze.py
# Breakdown-risk analysis for the Vossberg Mobility fleet.
#
# Key finding: total mileage and age do NOT separate the cars that broke down
# from those that did not (mean odometer ~53,450 km for both groups; age diff < 0.01 yr).
# The three factors that DO separate them are:
#   1. km_since_service  (broke-down mean 11,678 vs healthy mean 7,261 — biggest gap)
#   2. avg_daily_km      (broke-down mean 160 km/day vs 131 km/day)
#   3. load_factor       (broke-down mean 0.60 vs 0.51)
# The risk score below weights these three columns, normalised to 0-100.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# --- 1. Compare broke-down group vs healthy group for every numeric column ---
broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

feature_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

print("Factor comparison (broke_down=1 vs broke_down=0)")
print(f"{'column':<25}  {'broke mean':>12}  {'ok mean':>12}  {'diff':>10}")
print("-" * 65)
for col in feature_cols:
    b_mean = broke[col].mean()
    o_mean = ok[col].mean()
    print(f"{col:<25}  {b_mean:>12.2f}  {o_mean:>12.2f}  {b_mean - o_mean:>+10.2f}")

print()
print("NOTE: odometer_km and age_years show almost zero difference between groups.")
print("The predictive factors are km_since_service, avg_daily_km, and load_factor.\n")

# --- 2. Build a 0-100 risk score from the three predictive factors ---
# Normalise each column to [0, 1] relative to its observed min/max, then take
# a weighted average.  Weights reflect how large the group-mean gap was.
WEIGHTS = {
    "km_since_service": 0.50,
    "avg_daily_km":     0.30,
    "load_factor":      0.20,
}


def normalise(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - lo) / (hi - lo)


risk = pd.Series(0.0, index=df.index)
for col, weight in WEIGHTS.items():
    risk += normalise(df[col]) * weight

df["risk_score"] = (risk * 100).round(1)

# --- 3. Print cars ranked by risk, highest first ---
ranked = df[["car_id", "km_since_service", "avg_daily_km", "load_factor",
             "age_years", "odometer_km", "risk_score", "broke_down"]].sort_values(
    "risk_score", ascending=False
)

print("Fleet ranked by breakdown risk (highest first)")
print(f"{'car_id':<12}  {'risk':>6}  {'km_since_svc':>14}  {'avg_daily':>10}  "
      f"{'load':>6}  {'age':>5}  {'broke':>6}")
print("-" * 70)
for _, row in ranked.iterrows():
    print(
        f"{row['car_id']:<12}  {row['risk_score']:>6.1f}  "
        f"{int(row['km_since_service']):>14,}  {int(row['avg_daily_km']):>10,}  "
        f"{row['load_factor']:>6.2f}  {int(row['age_years']):>5}  "
        f"{'YES' if row['broke_down'] else 'no':>6}"
    )

print()
top10_breakdown_rate = ranked.head(10)["broke_down"].mean() * 100
print(f"Breakdown rate in top-10 risk cars : {top10_breakdown_rate:.0f}%")
print(f"Breakdown rate in bottom-10 risk cars: "
      f"{ranked.tail(10)['broke_down'].mean() * 100:.0f}%")
