# ERC location-level results

# Location-level analysis & cluster-robust inference

N=369 individuals across 72 distinct locations.

## Location summary — top 20 by fatalities

| Location                |   n | branch                  | type               |   dist_km |   n_joined |   pct_joined |   n_sof |   first_hour |   span_h |   mean_age |
|:------------------------|----:|:------------------------|:-------------------|----------:|-----------:|-------------:|--------:|-------------:|---------:|-----------:|
| Nahal Oz Post           |  52 | Military                | Military base/post |       4.2 |          0 |            0 |       0 |            1 |        6 |       20.3 |
| Be'eri                  |  32 | Military                | Civilian community |       7.5 |         27 |           84 |      11 |            2 |       32 |       32.3 |
| Kfar Aza                |  28 | Military                | Civilian community |       6.6 |         18 |           64 |      13 |            1 |        8 |       30.4 |
| Nova Festival           |  21 | Police                  | Festival           |       7.5 |          4 |           19 |       4 |            2 |        6 |       33   |
| Kissufim Outpost        |  15 | Military                | Military base/post |       3.5 |          0 |            0 |       3 |            2 |       11 |       20.8 |
| Erez Crossing           |  14 | Military                | Crossing           |       3.5 |          0 |            0 |       0 |            1 |        8 |       20.4 |
| Sufa Outpost            |  13 | Military                | Military base/post |       5.8 |          0 |            0 |       0 |            1 |        2 |       22.5 |
| Paga Outpost            |  13 | Military                | Military base/post |       4.3 |          1 |            8 |       0 |            1 |       12 |       20.3 |
| Sderot                  |  13 | Police                  | Civilian community |       9.8 |          7 |           54 |       2 |            2 |       27 |       40.5 |
| Kissufim                |  12 | Military                | Civilian community |       3.3 |          2 |           17 |       2 |            2 |        8 |       21.9 |
| Re'eim                  |  10 | Police                  | Military base/post |       7.5 |         10 |          100 |       4 |            2 |       13 |       32.5 |
| Ofakim                  |   8 | Police                  | Civilian community |      24.9 |          7 |           88 |       0 |            1 |        4 |       29.9 |
| Yiftach Outpost         |   8 | Military                | Military base/post |       2.7 |          2 |           25 |       1 |            1 |        7 |       20.9 |
| Urim Base               |   8 | Military                | Military base/post |      18.4 |          1 |           12 |       0 |            2 |        3 |       21.5 |
| Zikim Base              |   7 | Military                | Military base/post |       2.2 |          0 |            0 |       0 |            2 |        1 |       20.3 |
| Sha'ar HaNegev Junction |   7 | Police                  | Road/Junction      |       9.6 |          7 |          100 |       7 |            3 |        0 |       29.9 |
| Nir Itzhak              |   5 | Emergency Response Team | Civilian community |       7.2 |          5 |          100 |       0 |            2 |        2 |       42.8 |
| Mivtachim               |   5 | Emergency Response Team | Civilian community |      11.1 |          5 |          100 |       1 |            3 |        0 |       39.2 |
| Alumim                  |   5 | Military                | Civilian community |       7.3 |          5 |          100 |       2 |            5 |        2 |       29.2 |
| Near Re'im Junction     |   4 | Military                | Road/Junction      |       7.2 |          1 |           25 |       0 |            4 |        0 |       26   |


## Distribution of location size

- Locations with a single fatality: 32
- Locations with >=10 fatalities: 11
- Median fatalities per location: 2; max: 52 (Nahal Oz Post).
- Mean distance from border: 8.5 km (individual-weighted: 6.9 km).

## Fatalities by location type

| type               |   locations |   fatalities |
|:-------------------|------------:|-------------:|
| Beach/Open area    |           1 |            1 |
| Civilian community |          35 |          159 |
| Crossing           |           5 |           21 |
| Festival           |           2 |           22 |
| Military base/post |          17 |          143 |
| Road/Junction      |          12 |           23 |


## Distance vs location severity

Spearman correlation between a location's distance from the border and its fatality count: rho=-0.05, p=0.710 (location-level, n=70).

## Cluster-robust logistic regression — Joined (clustered by location)

Re-fits the individual-level model with **cluster-robust standard errors by location**, to check robustness to within-location correlation (multiple fatalities at the same site are not independent). The separated Branch term is dropped (Emergency Response Teams are completely separated on Joined); reference Service = Conscript. We compare naive vs clustered SEs.
| term                       |    OR |   SE_naive |   SE_clustered | 95% CI (clustered)   |   p (clustered) |
|:---------------------------|------:|-----------:|---------------:|:---------------------|----------------:|
| Intercept                  |  0.09 |      0.744 |          1.249 | 0.01-1.04            |           0.054 |
| C(Service)[T.Professional] |  2.96 |      0.512 |          0.75  | 0.68-12.88           |           0.148 |
| C(Service)[T.Reserves]     | 30.86 |      0.7   |          0.645 | 8.72-109.26          |           0     |
| SOF                        | 13.73 |      0.449 |          0.538 | 4.78-39.42           |           0     |
| Officer                    |  1.58 |      0.399 |          0.558 | 0.53-4.72            |           0.413 |
| Combat                     |  1.55 |      0.7   |          1.206 | 0.15-16.46           |           0.717 |
| Age_c                      |  1.09 |      0.021 |          0.029 | 1.03-1.15            |           0.004 |

n=366 individuals in 70 location clusters. The core conclusions survive clustering: **SOF (OR≈14), Reserves (OR≈31) and Age remain strong and significant** even with cluster-robust SEs — within-location correlation does not explain them away. Officer's independent effect attenuates to non-significance in this reduced model (it is collinear with service status and age, and in the full model its variance loaded onto the Branch terms that are dropped here for separation).