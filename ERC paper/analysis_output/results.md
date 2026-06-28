# ERC analysis results

# Sample

N = 369. Age present: 367. Time present: 366. Joined present: 368.

# A. Descriptive statistics


## Distribution: Branch

| Branch                  |   n |
|:------------------------|----:|
| Military                | 261 |
| Police                  |  58 |
| Emergency Response Team |  43 |
| Shin Bet                |   7 |


## Distribution: Service

| Service      |   n |
|:-------------|----:|
| Conscript    | 167 |
| Professional | 145 |
| Reserves     |  57 |


## Distribution: Wave

| Wave             |   n |
|:-----------------|----:|
| On-duty (wave 1) | 218 |
| Joined (wave 2)  | 150 |


## Age by Wave

| Wave             |   n |   mean |   median |   sd |   min |   max |
|:-----------------|----:|-------:|---------:|-----:|------:|------:|
| Joined (wave 2)  | 149 |   34.9 |       33 | 11.4 |    19 |    63 |
| On-duty (wave 1) | 217 |   22.8 |       20 |  6.9 |    18 |    58 |


## Age by Branch

| Branch                  |   n |   mean |   median |   sd |   min |   max |
|:------------------------|----:|-------:|---------:|-----:|------:|------:|
| Emergency Response Team |  43 |   44.6 |       44 |  9.8 |    27 |    63 |
| Military                | 260 |   22.7 |       21 |  5.9 |    18 |    53 |
| Police                  |  57 |   37   |       38 |  9.7 |    19 |    58 |
| Shin Bet                |   7 |   31.7 |       26 |  9.1 |    23 |    46 |


## Age by Service

| Service      |   n |   mean |   median |   sd |   min |   max |
|:-------------|----:|-------:|---------:|-----:|------:|------:|
| Conscript    | 166 |   20   |     20   |  1   |    18 |    24 |
| Professional | 144 |   31   |     28.5 |  9.7 |    19 |    58 |
| Reserves     |  57 |   41.6 |     39   | 10.9 |    19 |    63 |


## Age by SOF_b

| SOF_b   |   n |   mean |   median |   sd |   min |   max |
|:--------|----:|-------:|---------:|-----:|------:|------:|
| SOF     |  59 |   27.9 |       26 |  7.8 |    20 |    51 |
| non-SOF | 308 |   27.6 |       21 | 11.3 |    18 |    63 |


# B. Inferential statistics


## B1. Association with joining (chi-square / Fisher + effect size)

Each binary predictor is cross-tabulated with Joined; reported: test, p-value, Cramér's V, and odds ratio (joined vs not) with 95% CI.
| predictor   |   chi2 |   p(chi2) |   p(Fisher) |    V |   OR(join) | 95% CI     |
|:------------|-------:|----------:|------------:|-----:|-----------:|:-----------|
| SOF         |  53.81 |   2.2e-13 |     2.1e-13 | 0.38 |       9.98 | 4.92-20.22 |
| Officer     |  27.82 |   1.3e-07 |     2.2e-07 | 0.27 |       3.58 | 2.19-5.82  |
| Combat      |   4.79 |   0.029   |     0.034   | 0.11 |       2.73 | 1.04-7.17  |
| CT_bin      |  50.77 |   1e-12   |     1.5e-12 | 0.37 |       6.2  | 3.63-10.60 |


## B1b. Branch × Joined

| Branch                  |   0.0 |   1.0 |
|:------------------------|------:|------:|
| Emergency Response Team |     0 |    43 |
| Military                |   195 |    65 |
| Police                  |    22 |    36 |
| Shin Bet                |     1 |     6 |

chi2(3)=106.0, p=7.9e-23, Cramér's V=0.54

## B1b. Service × Joined

| Service      |   0.0 |   1.0 |
|:-------------|------:|------:|
| Conscript    |   152 |    14 |
| Professional |    62 |    83 |
| Reserves     |     4 |    53 |

chi2(2)=152.5, p=7.6e-34, Cramér's V=0.64

## B2. Multivariable logistic regression (Firth-penalized) — predicting Joined

Isolates the independent contribution of each factor (the bivariate comparisons are confounded: joiners are simultaneously older, more often officers, SOF and reserves). Reference: Service=Conscript, Branch=Military. **Firth penalization** is used because standard MLE does not converge here: Emergency Response Teams have 0 on-duty fatalities (complete separation — by definition they are local volunteers who joined), and Reserves are nearly separated. Firth yields finite, bias-reduced estimates.
| term                 |    OR | 95% CI       |     p |
|:---------------------|------:|:-------------|------:|
| Intercept            |  0.08 | 0.02-0.33    | 0     |
| SOF                  | 16.7  | 6.63-42.07   | 0     |
| Officer              |  3.43 | 1.29-9.12    | 0.013 |
| Combat               |  1.19 | 0.32-4.45    | 0.801 |
| Age_c                |  1.04 | 0.99-1.09    | 0.108 |
| Service:Professional |  1.36 | 0.42-4.40    | 0.608 |
| Service:Reserves     |  8.19 | 1.77-37.97   | 0.007 |
| Branch:Police        |  5.56 | 1.70-18.20   | 0.005 |
| Branch:ShinBet       |  3.28 | 0.26-41.90   | 0.36  |
| Branch:ERT           | 68.17 | 3.41-1364.04 | 0.006 |

n=366 (Firth-penalized logistic regression).

## B3. Time-to-death analysis

ANOVA on hours-to-death is questionable (right-skewed, coarse, and the sample is itself a selected/censored set — survivors are absent). We report a non-parametric Kruskal-Wallis test plus Kaplan-Meier curves and a Cox proportional-hazards model. NOTE: every observation is an event (death); true right-censoring (survivors) is NOT in the data, so survival estimates describe the fallen only — interpret as time-to-falling among fatalities, not population hazard.
- Kruskal-Wallis, Time by Wave: H=26.0, p=3.4e-07
- Kruskal-Wallis, Time by Branch: H=3.5, p=3.2e-01
- Kruskal-Wallis, Time by Service: H=18.0, p=1.2e-04
- Mann-Whitney, Time joined(4) vs on-duty(3): U=21036, p=3.4e-07

## B3b. Cox proportional-hazards (hazard of falling)

| term    |   HR |     p |
|:--------|-----:|------:|
| Joined  | 0.63 | 0.001 |
| SOF     | 0.73 | 0.047 |
| Officer | 0.86 | 0.24  |
| Age_c   | 1.01 | 0.039 |

HR<1 ⇒ lower instantaneous hazard ⇒ tended to fall later (lasted longer).

## B4. SOF over-representation — bounding argument with sensitivity

No exact open-source count of total IDF SOF personnel exists (classified). Instead we bound it: fatalities show SOF share = 16.3% (60/369). We compare against a *generous range* of assumed SOF shares of the 169,500 active IDF and report the rate ratio (RR). The conclusion is robust as long as true SOF share is a few percent.
| assumed SOF share of force   |   implied SOF headcount /169,500 | SOF share of fatalities   |   rate ratio |
|:-----------------------------|---------------------------------:|:--------------------------|-------------:|
| 0.5%                         |                              847 | 16.3%                     |         32.5 |
| 1.0%                         |                             1695 | 16.3%                     |         16.3 |
| 2.0%                         |                             3390 | 16.3%                     |          8.1 |
| 3.0%                         |                             5085 | 16.3%                     |          5.4 |
| 5.0%                         |                             8475 | 16.3%                     |          3.3 |

Even at a generous 5% assumed force share, SOF are over-represented among fatalities by a factor of ~3; at 1–2% the factor is ~8–16×.