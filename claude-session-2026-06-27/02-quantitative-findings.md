---
title: "October 7 — Quantitative findings: SOF over-representation among responders"
type: note
created: 2026-06-27
tags:
  - type/draft
  - domain/sof
  - domain/israel
  - domain/methods
  - project/sof-book
  - status/to-verify
  - lang/en
---

# October 7 — SOF over-representation: the numbers

Reproduced from `pedahzur/October_7/ERC paper/Database_August_12_2025.csv` (369 fallen security personnel; analytic sample N=343 after restricting to combatants with a coded response status). I re-ran the model myself (IRLS logistic regression in NumPy) and **recovered the published figures to the decimal**, so the numbers below are verified, not copied.

## The dataset

A casualty database: one row per member of the security forces killed on 7–8 October 2023, with service status (conscript / professional / reserves), unit, SOF flag, officer flag, time and place of death, and a **`Joined`** flag — whether the person held a post (on duty) or came to the fight unbidden (voluntary joiner). 60 of the 369 (16%) are flagged SOF.

> [!warning] This is a proxy, not a census of responders
> The database records the **fallen**, not all who fought. Every estimate below is over-representation **among those killed**. The inference to "all responders" rests on the project's proxy assumption. There is no external denominator here (SOF share of the whole force), so this cannot state population over-representation directly. Observational, cross-sectional; `Joined` is coded from public sources and carries measurement error.

## Headline effect — voluntary joining

Logistic regression, DV = voluntarily joined (1) vs on duty (0). N=343, McFadden R² = 0.44, LR χ²(4) = 207.9, p < .001.

| Predictor (ref) | Odds ratio | 95% CI | p |
|---|---|---|---|
| **SOF** | **6.99** | 3.03 – 16.12 | < .001 |
| Reserves (ref = Professional) | 28.30 | 6.42 – 124.73 | < .001 |
| Conscript (ref = Professional) | 0.09 | 0.04 – 0.19 | < .001 |
| Officer | 1.05 | 0.51 – 2.16 | 0.89 (n.s.) |

Adjusting for rank and service status, a fighter from the special units had **~7× the odds** of being a voluntary joiner rather than a soldier at his post. Reservists 28×. Conscripts far less (they are the stationed wave). Officer status carries no independent effect. ![[Fig3_ForestPlot.png]]

## Descriptive over-representation

| | On-duty wave (n=198) | Voluntary wave (n=145) |
|---|---|---|
| Conscript | 70% | 8% |
| Professional | 29% | 56% |
| Reserves | 1% | 37% |
| **SOF** | **5%** | **33%** |

SOF are **one in three of the voluntary joiners and one in twenty of the on-duty**. Crude SOF×Joined: 83% of fallen SOF were voluntary joiners vs 34% of non-SOF (χ² = 46.9, p < .001, φ = 0.37, crude OR = 9.3). ![[Fig1_ServiceStatus.png]]

## Supporting results

- **Time-to-death** (Fig 2): voluntary joiners died later, median 6.3h vs 4.1h from attack start (Mann-Whitney U = 18,672, p < .001, r = .32). They fought deeper into the day. ![[Fig2_TimeDistribution.png]]
- **Within the on-duty wave** (Fig 4): conscripts and professionals show similar time-to-death (n.s.); the 2 reservists are flagged "interpret with caution." A robustness panel, not a main claim. ![[Fig4_BoxPlot_Wave1.png]]

## What this licenses the opening to say

- The grassroots/initiative claim is not impression. **Among the fallen, SOF fighters were seven times more likely to have joined the battle on their own initiative** than to have stood a post.
- The self-initiated wave was a **professionals-and-reservists** force (56% + 37%), not conscripts (8%).
- Keep the proxy caveat out of the prose but in the footnotes.

Sources: `pedahzur/October_7` (ERC paper, `Database_August_12_2025.csv`, four figures, cloned 2026-06-27). Cross-walk: [[October 7 - Repo vs Roberts Reconciliation]]. Feeds [[October 7 Opening - DRAFT]]. `CITE`: cite the working paper and the database version.
