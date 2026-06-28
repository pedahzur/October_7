# Findings — Embedded Response Capacity (ERC), October 7, 2023

*A consolidated, manuscript-oriented synthesis of the empirical results. All numbers
are produced by `analysis_ERC.py` and `analysis_location.py` from
`Database_enriched.csv` (see `results.md` and `results_location.md` for full tables;
figures in `analysis_output/figures/`). This document is a research aid — verify the
age column and adapt wording before publication.*

## 1. Data and sample

The dataset records **N = 369** Israeli security personnel who fell on 7–8 October
2023, compiled from official open sources (IDF, Israel Police, Kan, Mapping the
Massacre) and cross-verified. For this analysis it was enriched with: a unique ID;
**age at death** located from open sources with two-source verification (367/369
found; 2 left blank); distance from the Gaza border (computed from coordinates); the
unit hierarchy split into command/division/brigade/battalion; and a location-type
classification. Two records lack coordinates (excluded from spatial analysis) and
three lack a time of death.

Composition of the fallen: **Military 261, Police 58, Emergency Response Team 43,
Shin Bet 7**; by service status **Conscript 167, Professional 145, Reserves 57**;
**Officers 94, Special-Operations Forces (SOF) 60 (16.3%)**. By mode of entry,
**218 were on duty** when the attack began and **150 joined** the fighting (one
unknown) — i.e. roughly **42% of those killed in combat had joined** the battle
without being on-duty at the scene.

## 2. Two waves of responders (H0)

The data strongly support two distinct waves. The mean time from the start of the
attack to death was **4 h for the on-duty wave vs 6.2 h for joiners**; a
non-parametric test confirms the difference in timing (Mann–Whitney, joined median 4
vs on-duty 3, *p* ≈ 3×10⁻⁷; Kruskal–Wallis by wave *H* = 26.0, *p* ≈ 3×10⁻⁷).

The waves differ sharply in **age** (Figure 1): joiners averaged **34.9** years
(median 33, SD 11.4) versus **22.8** for the on-duty (median 20, SD 6.9). Age tracks
service status — Conscripts 20.0, Professionals 31.0, Reserves 41.6 — and branch —
Emergency Response Team 44.6, Police 37.0, Shin Bet 31.7, Military 22.7.

## 3. Who joined? (H1) — bivariate

Every service-characteristic is strongly associated with joining (χ²/Fisher, with
odds ratios for joined vs not):

| Predictor | OR (95% CI) | effect / test |
|---|---|---|
| SOF | 9.98 (4.92–20.22) | χ² *p* = 2×10⁻¹³, Cramér's V = 0.38 |
| Counter-terror (CT>0) | 6.20 (3.63–10.60) | *p* = 1×10⁻¹² |
| Officer | 3.58 (2.19–5.82) | *p* = 1×10⁻⁷, V = 0.27 |
| Combat | 2.73 (1.04–7.17) | *p* = 0.029 |

Categorical predictors show large effects: **Service × Joined** χ²(2) = 152.5,
*p* ≈ 8×10⁻³⁴, V = 0.64; **Branch × Joined** χ²(3) = 106.0, *p* ≈ 8×10⁻²³, V = 0.54.
(Reserves were 35% of joiners but 1.8% of the on-duty; Emergency Response Teams, by
definition local volunteers, are 0% on-duty.)

## 4. Who joined? — multivariable (Firth)

Because Emergency Response Teams are completely separated on the outcome (and
Reserves nearly so), standard MLE does not converge; we use **Firth-penalized
logistic regression** (reference: Conscript, Military):

| Term | OR | 95% CI | *p* |
|---|---|---|---|
| **SOF** | **16.7** | 6.6–42.1 | <0.001 |
| **Reserves** | **8.2** | 1.8–38.0 | 0.007 |
| Police | 5.6 | 1.7–18.2 | 0.005 |
| **Officer** | **3.4** | 1.3–9.1 | 0.013 |
| Emergency Response Team | 68.2 | 3.4–1364 | 0.006 |
| Professional | 1.4 | 0.4–4.4 | 0.61 |
| Combat | 1.2 | 0.3–4.5 | 0.80 |
| Age (per year) | 1.04 | 0.99–1.09 | 0.11 |

**SOF membership is the strongest independent predictor of joining.** This holds
after adjusting for the confounding among joiner characteristics (joiners are
simultaneously older, more often officers, reserves and SOF).

## 5. Robustness to non-independence (location clustering)

Multiple fatalities at the same site are not independent (estimated within-location
correlation, exchangeable α = **0.355**). Two robustness checks (reduced model
without the separated Branch term, clustered by location, 70 clusters):

- **Cluster-robust SE logit:** SOF OR 13.7 (4.8–39.4, *p*<0.001); Reserves 30.9
  (8.7–109.3, *p*<0.001); Age 1.09 (1.03–1.15, *p* = 0.004).
- **GEE (exchangeable):** SOF OR 5.95 (*p*<0.001); Reserves 8.17 (*p*<0.001); Age
  1.05 (*p* = 0.005).

Both agree: the SOF, Reserves and Age effects are **not** artefacts of
within-location correlation. (Officer's independent effect attenuates once service
status and age are in the model — it is collinear with them.)

## 6. Time-to-death

Treating hours-to-death as time-to-event (events only — no survivors in the data, so
this describes the fallen, not a population hazard), a Cox model gives **Joined HR
0.63 (*p* = 0.001)** and **SOF HR 0.73 (*p* = 0.047)** — both fell *later* / lasted
longer — with Age HR 1.01 (*p* = 0.039). Differences in timing are significant by
wave and by service status, but not by branch (Kruskal–Wallis *H* = 3.5, *p* = 0.32).

## 7. SOF over-representation (bounding argument)

No exact open-source count of total IDF SOF strength exists (classified), so we bound
it. SOF are **16.3%** of the fallen. Against a generous range of assumed SOF shares of
the 169,500-strong active IDF (IISS 2023):

| Assumed SOF share of force | Rate ratio (fatalities : force) |
|---|---|
| 5% | 3.3× |
| 3% | 5.4× |
| 2% | 8.1× |
| 1% | 16.3× |

The conclusion is robust: even at a generous 5% the over-representation is ~3×, and
at a realistic 1–2% it is ~8–16×. (See `Force_composition_baselines.md` for the
denominator sourcing.)

## 8. Location-level view

Across **72 locations** (median 2 fatalities; 32 single-fatality sites; 11 sites with
≥10), the two-wave structure is visible site-by-site (Figures 7–8):

| Location | Fallen | % joined | Mean age | Character |
|---|---|---|---|---|
| Nahal Oz Post | 52 | 0% | 20.3 | base overrun — first wave (conscripts) |
| Be'eri | 32 | 84% | 32.3 | community — second wave (joiners) |
| Kfar Aza | 28 | 64% | 30.4 | community — mixed |
| Sha'ar HaNegev Junction | 7 | 100% | 29.9 | all SOF — joiners |

Military **bases/outposts** clustered the young, on-duty first wave; **civilian
communities, roads and junctions** drew the older joiners and SOF. A location's
distance from the border was **not** correlated with its fatality count
(Spearman ρ = −0.05, *p* = 0.71) — the fighting was severe both at the fence and
deep inside (e.g. Ofakim, ~25 km).

## 9. Interpretation (ERC)

The pattern is consistent with Embedded Response Capacity: a younger, stationed first
wave fought and fell at the border installations, while an older, more professional
second wave — disproportionately reserves, officers and SOF — self-mobilized into the
communities and road ambushes, lasted longer, and engaged the attackers across many
sites. The defining feature of the joiners is not merely that they came, but **who**
they were: trained, specialized personnel able to switch instantly from routine to
crisis without command direction.

## 10. Limitations

1. **Proxy / survivor bias** — fatalities proxy for responders; survivors (different
   by construction) are absent, so survival results describe the fallen only.
2. **Denominator** — over-representation rests on the bounding argument; exact SOF
   strength is classified.
3. **Non-independence** — addressed via clustered SE and GEE, but a full multilevel
   model could be added for the manuscript.
4. **Measurement** — time of death is coarse and partly estimated; small cells
   (Shin Bet n = 7); the age column was sourced by automated cross-referencing and
   should be manually reviewed.
