# What I checked, and what the agent got wrong

## What the agent got wrong

The agent's first instinct when looking at the breakdown-risk analysis was to use total
mileage (`odometer_km`) as the primary predictor — which is the obvious assumption and
also the wrong one. I caught this by asking it to compare every column between the
broke-down group and the healthy group before touching any code. The numbers showed that
the mean odometer reading was almost identical in both groups (53,448 km for cars that
broke vs 53,302 km for cars that did not — a difference of under 150 km across 120 cars).
Age in years was even closer: 5.88 vs 5.89, essentially zero. The agent would have built
a score that rewarded old, high-mileage cars as high-risk and called the job done. That
score would have been nearly useless.

I also verified the `km_to_miles` fix manually before accepting it. The original constant
was 1.609, which is the number of kilometres per mile — the *inverse* of what was needed.
The corrected constant is 0.621371. I checked 100 km → 62.1 miles in the verify output
to confirm the right direction.

## What I checked before I accepted its work

For the wear bug: I ran `python verify.py` and read the "Wear is no longer floored to 0"
line, which showed 99.3 % for a car at 14,900 of 15,000 km. I then looked at the actual
`wear_percent` function in `km_wachter.py` to confirm it was a straight ratio with no
integer division or floor operation. The old code used `//` (integer floor division),
which zeroed any result below 1 %. The fix replaced that with `/`.

For the 80 % rule: `verify.py` has a dedicated check — "The 15000 km / 80% rules are
untouched" — which reads `SERVICE_INTERVAL_KM` and `WARN_AT_PERCENT` directly from the
module. Both printed as expected (15000 and 80). I also checked `settings.cfg` via the
config-rules check to make sure the file values matched the code values.

For the missing-reading fix: the check "A missing reading is handled" passes a car dict
with no `last_service_km` key. It expects `needs_service` to return `False`. I read the
function body to confirm it uses `car.get("last_service_km", car["odometer"])`, which
makes the km-since-service calculation produce zero when the key is absent, so the wear
percentage is 0 % and no service flag fires.

## What the data actually said

The two columns that look like obvious predictors — total odometer reading and age in
years — turned out to have almost no predictive value. Cars that later broke down had
a mean odometer of 53,448 km; cars that did not had a mean of 53,302 km. Age was 5.88
vs 5.89 years. Both differences are well within noise.

The three columns that actually separate the two groups are:

1. **km_since_service** — the biggest gap by far: 11,678 km average for cars that broke
   down vs 7,261 km for healthy cars. A car that has been running a long time since its
   last service is far more likely to fail, regardless of how old or how many total
   kilometres it has accumulated.

2. **avg_daily_km** — broke-down cars were driven harder on average (160 km/day vs
   131 km/day). High daily usage puts more stress on components between services.

3. **load_factor** — broke-down cars carried heavier loads on average (0.60 vs 0.51).
   This is a secondary but real contributor.

The risk score built from these three factors (weighted 50 / 30 / 20) puts the top-10
highest-risk cars at an 80 % actual breakdown rate, while the bottom-10 have a 0 %
breakdown rate. That validates the approach: the score would flag risky cars well before
the 80 % service-interval rule would ever trigger.
