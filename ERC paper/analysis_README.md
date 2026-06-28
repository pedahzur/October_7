# ERC Analysis Pipeline

`analysis_ERC.py` runs the descriptive + inferential statistics on
`Database_enriched.csv` and produces infographic figures.

## How to run
```bash
pip install pandas numpy scipy statsmodels matplotlib tabulate
python3 analysis_ERC.py
```
Outputs go to `analysis_output/`:
- `results.md` — all numeric results (tables for every test/model)
- `figures/*.png` — infographics

## What it computes

### Descriptive (infographics)
| Figure | Content |
|---|---|
| `fig1_age_by_wave.png` | Age histogram, on-duty vs joined — shows the bimodal two-wave pattern |
| `fig2_mean_age.png` | Mean age by branch and by service status |
| `fig3_composition.png` | Pie charts: branch / service / SOF / officer composition of the fallen |
| `fig4_location_distance.png` | Fatalities by location type; distance-from-border distribution |
| `fig5_time_by_wave.png` | Hours-from-attack-to-death, by wave |
| `fig6_km_by_wave.png` | Kaplan-Meier "time-to-falling" curves by wave |

### Inferential
- **B1 — χ² / Fisher** for each binary predictor (SOF, Officer, Combat, CT) vs `Joined`,
  with **Cramér's V** (effect size) and **odds ratios + 95% CI**. Multi-category
  predictors (Branch, Service) reported with full cross-tabs.
- **B2 — Firth-penalized logistic regression** predicting `Joined` from SOF, Officer,
  Combat, Age, Service and Branch. Firth is used because standard MLE does **not**
  converge (Emergency Response Teams are completely separated — 0 on-duty fatalities;
  Reserves nearly so). Firth gives finite, bias-reduced estimates.
- **B3 — time-to-death**: non-parametric **Kruskal-Wallis** / **Mann-Whitney**
  (preferred over ANOVA: the variable is skewed, coarse, and the sample is a selected
  set), plus **Kaplan-Meier** and a **Cox proportional-hazards** model.
- **B4 — SOF over-representation bounding argument** with a sensitivity table over a
  generous range of assumed SOF force shares (since the true SOF headcount is classified).

## Key results (see `results.md` for full tables)
- **Two waves confirmed**: joined mean age 34.9 vs on-duty 22.8; Mann-Whitney p≈3e-7.
- **SOF is the strongest independent predictor of joining**: adjusted OR ≈ 16.7
  (Firth, p<0.001); Reserves OR ≈ 8.2; Officer OR ≈ 3.4.
- **SOF over-representation is robust**: even assuming a generous 5% SOF force share,
  SOF are over-represented among fatalities ~3×; at 1–2%, ~8–16×.
- Cox: joined and SOF have hazard ratios <1 (fell later / lasted longer).

## Important caveats (read before publishing)
1. **No survivors in the data** → the Kaplan-Meier/Cox results describe *time-to-falling
   among fatalities*, not a population hazard. Frame accordingly.
2. **Non-independence**: multiple fatalities share a unit/location; consider clustered
   standard errors or multilevel models for a final published version.
3. **Small cells**: Shin Bet n=7 — interpret its estimates cautiously.
4. **Denominators**: the over-representation claim relies on the bounding argument in B4
   (see `Force_composition_baselines.md`), not on an exact SOF count.
5. The `Age` column was sourced by automated cross-referencing — review before publishing.
