# Manuscript sections (draft)

*Draft prose for integration into the ERC paper. Written in the manuscript's voice
and grounded in the project's data and computed results (`Database_enriched.csv`,
`results.md`, `results_location.md`, `Force_composition_baselines.md`). All
quantitative claims are reproducible from the analysis scripts. Verify the age column
before submission.*

---

## Methodology

The empirical strategy of this study follows from the central problem the October 7
attack poses for the researcher: there exists no unified, authoritative roster of the
forces that responded. The fog of war prevented the creation of such a record in real
time, and where partial logs exist they remain classified. We therefore adopt a
**proxy design**, using data on the security personnel who were *killed* on 7–8
October 2023 to infer which units, branches and types of fighter were present and
engaged across the Gaza envelope. The logic is that the affiliations, locations and
timing of the fallen reveal the composition of the responding force, and in
particular allow us to distinguish those who were stationed at the scene when the
attack began from those who joined the fighting afterwards.

The design has a known cost, which we state at the outset. The fallen are a
*selected* subset of responders; survivors may differ systematically from those who
died (survivor bias). We treat the resulting estimates as describing the population of
fatalities rather than the full responding force, and we are explicit throughout about
which inferences the data can and cannot support. The proxy is nonetheless
well-suited to our research question, which concerns the *characteristics* of the
responding forces rather than counts of survivors, and it is the highest-resolution
evidence available from open sources.

The unit of analysis is the individual fallen security person. Each case is coded for
personal data (name, age), organizational affiliation (military, police, Shin Bet,
emergency-response team), specific unit, service status (conscript, professional,
reserve), a set of binary service characteristics (combat/non-combat, officer/non-
officer, special-operations/not, counter-terror/not), place of death (with
coordinates) and time of death (hours since the 06:29 onset of the attack). The
analytically central variable is the **mode of entry**: a binary indicator of whether
the individual was on duty at the scene when the attack began or arrived to fight
without a clear order to do so ("joined"). This variable operationalizes the paper's
distinction between a first, stationed wave and a second, self-mobilized wave of
responders.

Three hypotheses structure the analysis. **H0:** there were two waves of responders,
one composed of those stationed at the border and one of volunteers who joined the
fighting. **H1:** the most effective combat forces joined voluntarily rather than
being summoned by senior command. **H2:** the basic characteristics of Embedded
Response Capacity (ERC) — joint training, decentralized execution, urban-warfare
proficiency, adaptability and ad-hoc teaming — are reflected in the self-joined
forces.

## Data collection

The dataset was assembled from official open sources and cross-verified across them.
The IDF's dedicated memorial mini-site provided each soldier's name (Hebrew and
English), age, rank, unit and date of death (301 cases; gender is inferable from
gendered Hebrew). The Israel Police memorial site supplied parallel records for fallen
officers (68 cases), including rank, unit and place of burial. Two map-based public
resources — Kan's October-7 project and the civilian "Mapping the Massacre"
initiative — were used to place individuals at specific events and locations; both are
narrative and uneven in coverage, and were treated as supplementary. Where the
official sources did not fix the exact place or time of death, we triangulated using
press reporting, the published security-agency operational probes, and family
testimony regarding when contact was lost. The database grew out of an initial
compilation of the fallen — 182 soldiers extracted from the government's *Swords of
Iron* casualties page on October 26, 2024 — which was subsequently expanded and
cross-verified against the sources above. That working file is preserved, with its
documentation, in the repository's `Evolving-Paradigms/` folder.

For the present study the verified records were **enriched** with several derived and
externally sourced fields. Age at death — recorded in principle but missing from the
working file for many cases — was located from open sources, primarily the *Times of
Israel* obituary series, and accepted only when **two independent sources agreed**;
this yielded ages for 367 of 369 cases (two unresolved cases were left blank, and one
further case rests on a single source). Distance from the Gaza border was computed
from each case's coordinates. The composite unit string was parsed into its
hierarchical levels (command, division, brigade, battalion). Locations were
classified by type (military base/outpost, civilian community, road/junction,
crossing, festival, open area). A reproducible codebook documents every variable.

## Sample

The sample comprises **N = 369** security personnel killed on 7–8 October 2023.
By branch, the fallen were **Military (261), Police (58), Emergency-Response Team
(43)** and **Shin Bet (7)**. By service status they were **Conscripts (167),
Professionals (145)** and **Reserves (57)**. **Ninety-four were officers** and
**sixty (16.3%) belonged to special-operations forces**. Ages ranged from 18 to 63.

The variable of central interest divides the sample cleanly: **218 individuals were
on duty** at the scene when the attack began, while **150 joined** the fighting
afterwards (one case unknown). Restricting to the 344 killed in combat — excluding
those killed as non-combatants in their homes or at the Nova festival — roughly
**42% had joined**, confirming that the second wave was not a marginal phenomenon but
a substantial share of those who fought and fell. Two cases lack coordinates and
three lack a recorded time of death; these are handled by listwise exclusion in the
relevant analyses.

## Analyses

We proceeded in three stages: description, association, and adjusted/robust
inference, followed by a location-level analysis.

For **description**, we summarized the composition of the fallen and the distribution
of age, timing, location type and distance from the border, overall and by wave,
branch and service status. For **association**, each binary service characteristic was
cross-tabulated with mode of entry, and we report χ²/Fisher tests with Cramér's V as
an effect size and odds ratios with 95% confidence intervals; multi-category
predictors (branch, service) are reported with the full contingency tables.

Because several predictors are strongly confounded — joiners tend to be
simultaneously older, more often officers, reserves and SOF — we estimated a
**multivariable logistic regression** of joining. Standard maximum likelihood does
not converge here, because emergency-response teams are completely separated on the
outcome (they are, by construction, local volunteers who joined) and reserves are
nearly so; we therefore used **Firth-penalized logistic regression**, which yields
finite, bias-reduced estimates under separation.

Because multiple fatalities at the same site are not independent observations, we
assessed robustness to within-location dependence in two ways: a logistic model with
**cluster-robust standard errors** by location, and a **generalized estimating
equations** (GEE) model with an exchangeable working correlation. Time from the onset
of the attack to death was analyzed non-parametrically (Kruskal–Wallis, Mann–Whitney)
and with Kaplan–Meier and Cox models, with the explicit caveat that the data contain
events only (no survivors), so these describe time-to-falling among the fatalities
rather than a population hazard. Finally, because no open-source count of total SOF
strength exists, the over-representation of special-operations forces was assessed
with a **bounding argument** and sensitivity analysis rather than a single point
estimate. Analyses were conducted in Python (pandas, SciPy, statsmodels).

## Findings

**Two waves (H0).** The data show two clearly distinct waves of responders. Those who
joined fell, on average, two hours later than those on duty (means of 6.2 vs 4.0 hours
from the onset of the attack; Mann–Whitney *p* ≈ 3×10⁻⁷), the lag corresponding to
the time it took to reach the fighting. The waves differ markedly in age: joiners
averaged **34.9** years (median 33) against **22.8** for the stationed wave (median
20) — a near-bimodal distribution in which the first wave clusters at the conscript
age of twenty while the second is spread across the thirties, forties and beyond.
Age in turn tracks service status (conscripts 20.0, professionals 31.0, reserves
41.6) and branch (emergency-response teams 44.6, police 37.0, military 22.7).

**Who joined (H1).** At the bivariate level, every service characteristic is strongly
associated with joining: special-operations membership (OR 9.98, 95% CI 4.92–20.22),
counter-terror role (OR 6.20), officer status (OR 3.58) and combat role (OR 2.73), all
significant; service status and branch show large effects (Cramér's V = 0.64 and 0.54
respectively). In the adjusted Firth model, **special-operations membership is the
strongest independent predictor of joining (OR ≈ 16.7, *p* < 0.001)**, followed by
reserve status (OR ≈ 8.2) and officer rank (OR ≈ 3.4). These effects survive
correction for the non-independence of fatalities within locations: under
cluster-robust standard errors and under a GEE model — with a non-trivial estimated
within-location correlation (α = 0.355) — the SOF, reserve and age effects remain
significant. The Cox analysis points the same way: joiners and SOF personnel have
hazard ratios below one (HR 0.63 and 0.73), i.e. they fell later and lasted longer
than the stationed conscripts. Taken together, the second wave was disproportionately
composed of the most highly trained and specialized personnel, and these were the
forces that engaged the enemy across the longest span of the day.

**Over-representation of special operations.** Special-operations personnel are
**16.3%** of the fallen. Because their true share of the force is classified, we bound
the comparison: even on a generous assumption that SOF constitute 5% of the
169,500-strong active IDF, they are over-represented among the fatalities by roughly
threefold; at a more realistic 1–2% the factor is eight- to sixteen-fold. The
conclusion — pronounced over-representation — is robust across the plausible range and
does not depend on a precise denominator.

**The location-level view (H2).** Aggregating to the 72 distinct locations makes the
two-wave structure concrete. The military bases and outposts overrun in the opening
hours concentrated the young, stationed first wave — at Nahal Oz Post, the single
deadliest site, all 52 fallen were on duty, with a mean age of twenty. The civilian
communities, roads and junctions, by contrast, drew the older, self-mobilized second
wave: at Be'eri 84% of the 32 fallen had joined (mean age 32), and at the Sha'ar
HaNegev junction all of the fallen had joined and all were special-operations
personnel. A location's distance from the border was uncorrelated with its fatality
count (Spearman ρ = −0.05, *p* = 0.71): the fighting was severe both at the fence and
deep inside Israeli territory, as far as Ofakim some twenty-five kilometres away. This
distribution is the empirical signature of a "defensive swarm" — a dispersed,
self-organizing response that met the attackers at many points at once — and it is
the self-joined forces, rich in officers and special-operations personnel, who
produced it. The composition of the joiners matches the ERC profile: the great
majority belong to the IDF and to emergency-response teams trained in the same
facilities and sharing a common operational language (joint training); they fought in
small, isolated teams while the Gaza Division was non-functional (decentralized
execution); they were overwhelmingly combat-trained and urban-warfare-proficient; the
second wave adapted to fight across the communities where the first could not; and
they formed ad-hoc squads organized by location rather than by their organic units.

## Conclusions

The October 7 paradox — an effective response amid the collapse of command and
control — is resolved, on this evidence, by Embedded Response Capacity. The data
support all three hypotheses. There were two waves of responders (H0): a younger,
stationed first wave that fought and fell at the border installations, and an older,
more professional second wave that self-mobilized into the communities and road
ambushes. The most effective forces joined voluntarily (H1): the joiners were
disproportionately reserves, officers and special-operations personnel, they engaged
the enemy across more sites and a longer span of the day, and special-operations
personnel are over-represented among the fallen by a wide and robust margin. And the
characteristics of ERC are reflected in those self-joined forces (H2): shared
training and operational language, decentralized execution under a defunct command,
urban-warfare proficiency, instant adaptation from routine to crisis, and ad-hoc
teaming.

The broader implication is that the resilience on display was not institutional in the
conventional sense — the institutions' command, intelligence and communications all
failed — but was instead embedded in the trained individuals and small teams who could
act effectively without direction. For states confronting swarm terrorism, the
practical lesson is to cultivate this capacity deliberately: to maintain decentralized
reserve and local-response units, to train relevant personnel to act independently in
crisis, to equip local forces against commando-style assault, and to instill in
internal-security forces an understanding of military-scale scenarios and an ethos of
joining when needed.

These conclusions are bounded by the study's design. The analysis rests on a proxy of
fatalities and is therefore subject to possible survivor bias; the over-representation
claim relies on a bounding argument because the exact force denominator is classified;
the timing variable is coarse and partly estimated; some subgroups (notably Shin Bet,
n = 7) are small; and the externally sourced ages, while doubly verified, warrant a
final manual check. Two avenues follow directly from the present work: linking each
location to an independent measure of severity (civilians killed and abducted) to test
the relationship between the responding forces and outcomes, and a fully specified
multilevel model of the determinants of time-to-control. Neither alters the core
finding here — that where technology, hierarchy and intelligence failed on 7 October
2023, trained individuals, acting on their own initiative, did not.
