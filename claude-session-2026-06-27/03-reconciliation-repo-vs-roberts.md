---
title: "October 7 — pedahzur/October_7 data vs Roberts Report timeline"
type: note
created: 2026-06-27
tags:
  - type/draft
  - domain/sof
  - domain/israel
  - project/sof-book
  - status/to-verify
  - lang/en
---

# October 7 — Reconciling the repo data with the Roberts timeline

Cross-walk of the `pedahzur/October_7` datasets (`Units.csv`, `Locations.csv`, README argument) against [[2023-10-07 October 7 Attack Timeline|the Roberts Report timeline]]. The repo's research question is the book opening's claim, formalized: *how do SOF contribute to a state's response to a violent non-state attack?* Its core finding is a **disproportionate presence of special-unit fighters among the responders**, many of whom **self-initiated**.

## Elite-unit cross-walk

| Unit | Roberts (arrival at site) | Repo arrival / sites | Repo: did they initiate? |
|---|---|---|---|
| Sayeret Matkal | Kfar Aza ~10:30 | 08:00 · Kfar Aza, Be'eri | **Yes** — after the first news |
| Duvdevan | Kfar Aza ~10:30 | 08:00 · Kfar Aza | **Yes** — many arrived in the first hours and acted alone |
| Shayetet 13 | Sufa 14:30 (rescues 250); Nir Oz 14:15 (naval) | Sufa base, Nahal Oz base, Zikim Beach | ~30 soldiers met the attack at Nahal Oz |
| Shaldag | Holit 15:30 | 09:00 · Re'im base (06:45), Be'eri, Alumim, Holit | **Yes** — by commander, inserted by helicopter |
| LOTAR | Sufa ~13:00 | 08:00 · Orim base (07:30), Holit, Sufa, Nir Yitzhak | **No** — received an order |
| Unit 669 | (not named) | 08:00 · Kisufim | **Yes** — organized themselves, arrived without a clear mission |
| Yamam (police CT) | (not named) | 06:45 · Ofakim, Sderot, Be'eri, Nahal Oz | **Yes** — arrived fast; ended the Ofakim hostage standoff |
| Shabak | (not named) | 06:30 · Mefalsim | **Yes** — initiated the fight as a team |

## Three findings

**1. The sources agree on WHO and WHERE; they differ on WHEN — and the difference is the argument.** The repo records early scramble and first-area arrival (06:30–09:00, often on the fighters' own initiative). Roberts records arrival at the contested kibbutzim hours later (10:30–15:30). The gap is the cost of fighting south through ambushed roads and of working several sites in sequence. This is the **cost-of-distance** problem in miniature: elite fighters self-mobilized within ~90 minutes, but distance, ambushes, and a saturated battlespace meant they reached the worst-hit communities late. See [[40 Notes/SOF/Cost-of-distance dilemma|cost-of-distance]].

**2. Initiative is unit-variable, and it tracks the elite units.** Self-initiated per the repo: Sayeret Matkal, Duvdevan, Unit 669, Sayeret Nahal, Yamam, Yamas, Shabak, Division 99. Waited for orders or were slow: LOTAR ("received an order"), Caracal ("no order, did not respond in time"), Maglan ("did not come out immediately"), Bislamach ("did not act until 3 days after"). The README's disproportion claim holds here: the units whose culture prizes initiative are the ones that moved without being told.

**3. Severity tracks *any* effective armed response, not just a named unit.** From `Locations.csv`, worst tolls: Nova 364 killed / 40 taken (Paratroopers, late); Be'eri 125 / 25; Kfar Aza 74 / 19; **Nir Oz 37 / 75 taken — "No military response."** But "no military response" is **not** uniformly worst: where a civilian standby squad engaged (Zikim, Gevim, Yated, Ein HaBesor, Magen), the toll was ~0. So the operative variable is whether *any* trained armed response, a unit **or** a standby squad, made contact — which refines the README's hypothesis (Nir Oz at the top is right; the bottom is "standby squad held," not merely "a unit came").

## Discrepancies to resolve before publication

- **Times:** repo "arrival" (scramble/first-area) vs Roberts "arrival at site." Decide a convention and label every time as one or the other. `status/to-verify`.
- **Shaldag location:** Roberts puts the named arrival at Holit (15:30); the repo spreads Shaldag across Re'im base, Be'eri, Alumim, Holit. Likely different sub-teams; confirm.
- **LOTAR initiative:** repo says "received an order" — the one elite unit marked *not* self-initiated. Worth a line in the book, since it cuts against the clean thesis.

## Quantitative backbone (now analyzed)

The repo's `ERC paper/` dataset has been reproduced and verified: see [[October 7 - Quantitative Findings (SOF over-representation)]]. Headline: among the fallen, SOF carried ~7× the odds of being a voluntary joiner (logistic OR 6.99, 95% CI 3.0–16.1, p<.001; N=343), and were 33% of the voluntary wave vs 5% of the on-duty. Proxy caveat (casualty data, not all responders) recorded in that note.

Sources: `pedahzur/October_7` (cloned 2026-06-27) · [[2023-10-07 October 7 Attack Timeline]] · feeds [[October 7 Opening - DRAFT]].
