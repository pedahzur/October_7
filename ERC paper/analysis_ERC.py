#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ERC analysis pipeline
=====================
Runs descriptive + inferential statistics on Database_enriched.csv and
produces infographic figures.

Outputs (written to ./analysis_output/):
  - figures/*.png            infographics (descriptive)
  - results.md               full numeric results (tests, models)
Dependencies: pandas, numpy, scipy, statsmodels, matplotlib
Run:  python3 analysis_ERC.py
"""
import os, math, textwrap
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.duration.hazard_regression import PHReg
from statsmodels.duration.survfunc import SurvfuncRight
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Database_enriched.csv")
OUT = os.path.join(HERE, "analysis_output")
FIG = os.path.join(OUT, "figures")
os.makedirs(FIG, exist_ok=True)

PALETTE = ["#1f4e79", "#c0392b", "#2e8b57", "#d4a017", "#6a5acd", "#7f8c8d"]
plt.rcParams.update({"figure.dpi": 130, "font.size": 11, "axes.grid": True,
                     "grid.alpha": .25, "axes.edgecolor": "#444"})


def firth_logit(X, y, max_iter=200, tol=1e-8):
    """Firth penalized logistic regression (handles complete/quasi separation).
    X must already include an intercept column. Returns (beta, se)."""
    n, k = X.shape
    beta = np.zeros(k)
    XtWX_inv = np.eye(k)
    for _ in range(max_iter):
        eta = np.clip(X @ beta, -30, 30)
        pr = 1.0 / (1.0 + np.exp(-eta))
        W = pr * (1 - pr)
        XtWX = X.T @ (X * W[:, None])
        XtWX_inv = np.linalg.pinv(XtWX)
        Xw = X * np.sqrt(W)[:, None]
        h = np.einsum("ij,jk,ik->i", Xw, XtWX_inv, Xw)   # hat diagonal
        U = X.T @ (y - pr + h * (0.5 - pr))               # Jeffreys-penalized score
        step = XtWX_inv @ U
        beta = beta + step
        if np.max(np.abs(step)) < tol:
            break
    se = np.sqrt(np.diag(XtWX_inv))
    return beta, se

md = []  # results.md lines
def h(s, lvl=2): md.append("\n" + "#"*lvl + " " + s + "\n")
def p(s=""): md.append(s)
def tbl(df):
    md.append(df.to_markdown(index=False))
    md.append("")

# ----------------------------------------------------------------------------
# Load & prepare
# ----------------------------------------------------------------------------
df = pd.read_csv(SRC)
# canonical column aliases
df = df.rename(columns={"Conscript/Reserves/ Professional": "Service"})
for c in ["CT", "SOF", "Officer", "Combat", "Joined", "Gender"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df["Time"] = pd.to_numeric(df["Time"], errors="coerce")           # hours since attack start
df["Dist"] = pd.to_numeric(df["Distance_from_border_km"], errors="coerce")
df["SOF_b"] = df["SOF"].map({0: "non-SOF", 1: "SOF"})
df["Wave"] = df["Joined"].map({0: "On-duty (wave 1)", 1: "Joined (wave 2)"})

N = len(df)
h("Sample", 1)
p(f"N = {N}. Age present: {df['Age'].notna().sum()}. "
  f"Time present: {df['Time'].notna().sum()}. "
  f"Joined present: {df['Joined'].notna().sum()}.")

# ============================================================================
# A. DESCRIPTIVE  (+ infographics)
# ============================================================================
h("A. Descriptive statistics", 1)

# A1 — headline counts
counts = {
    "Branch": df["Branch"].value_counts(),
    "Service": df["Service"].value_counts(),
    "Wave": df["Wave"].value_counts(dropna=True),
}
for k, v in counts.items():
    h(f"Distribution: {k}")
    tbl(v.rename_axis(k).reset_index(name="n"))

# A2 — age summary by group
def age_summary(by):
    g = df.dropna(subset=["Age"]).groupby(by)["Age"]
    out = g.agg(n="count", mean="mean", median="median", sd="std",
                min="min", max="max").round(1).reset_index()
    return out
for by in ["Wave", "Branch", "Service", "SOF_b"]:
    h(f"Age by {by}")
    tbl(age_summary(by))

# ---- FIGURE 1: age histogram overall + by wave
fig, ax = plt.subplots(figsize=(8, 4.5))
bins = range(16, 66, 3)
for i, (lab, sub) in enumerate(df.dropna(subset=["Age"]).groupby("Wave")):
    ax.hist(sub["Age"], bins=bins, alpha=.65, label=lab, color=PALETTE[i])
ax.set_title("Age distribution of fallen security personnel, by wave")
ax.set_xlabel("Age at death"); ax.set_ylabel("Count"); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_age_by_wave.png")); plt.close(fig)

# ---- FIGURE 2: mean age by branch / service (bar)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, by in zip(axes, ["Branch", "Service"]):
    s = age_summary(by).sort_values("mean")
    ax.barh(s[by], s["mean"], color=PALETTE[:len(s)])
    for y, (m, n) in enumerate(zip(s["mean"], s["n"])):
        ax.text(m + .3, y, f"{m:.0f} (n={n})", va="center", fontsize=9)
    ax.set_title(f"Mean age by {by}"); ax.set_xlabel("Mean age")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig2_mean_age.png")); plt.close(fig)

# ---- FIGURE 3: composition of fallen (branch / service / SOF / officer)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, col, title in zip(
        axes.ravel(),
        ["Branch", "Service", "SOF_b", "Officer"],
        ["Branch", "Service status", "Special Ops Forces", "Officer"]):
    vc = df[col].value_counts()
    ax.pie(vc, labels=[str(x) for x in vc.index], autopct="%1.0f%%",
           colors=PALETTE, startangle=90, textprops={"fontsize": 9})
    ax.set_title(title)
fig.suptitle("Composition of fallen security personnel (N=369)", y=1.0)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig3_composition.png")); plt.close(fig)

# ---- FIGURE 4: location type & distance from border
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
lt = df["Location_type"].value_counts()
axes[0].barh(lt.index[::-1], lt.values[::-1], color=PALETTE[0])
axes[0].set_title("Fatalities by location type")
axes[1].hist(df["Dist"].dropna(), bins=20, color=PALETTE[2])
axes[1].axvline(df["Dist"].median(), color=PALETTE[1], ls="--",
                label=f"median {df['Dist'].median():.1f} km")
axes[1].set_title("Distance from Gaza border (km)")
axes[1].set_xlabel("km"); axes[1].legend()
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_location_distance.png")); plt.close(fig)

# ---- FIGURE 5: time-of-death distribution by wave
fig, ax = plt.subplots(figsize=(8, 4.5))
for i, (lab, sub) in enumerate(df.dropna(subset=["Time"]).groupby("Wave")):
    ax.hist(sub["Time"], bins=range(0, 25), alpha=.6, label=lab, color=PALETTE[i])
ax.set_title("Hours from attack start to death, by wave")
ax.set_xlabel("Hour of attack"); ax.set_ylabel("Count"); ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig5_time_by_wave.png")); plt.close(fig)

# ============================================================================
# B. INFERENTIAL
# ============================================================================
h("B. Inferential statistics", 1)

def cramers_v(chi2, n, r, k):
    phi2 = chi2 / n
    return math.sqrt(phi2 / min(r - 1, k - 1)) if min(r - 1, k - 1) > 0 else float("nan")

# B1 — chi-square / Fisher: Joined vs categorical, with effect size & OR
h("B1. Association with joining (chi-square / Fisher + effect size)")
p("Each binary predictor is cross-tabulated with Joined; reported: test, "
  "p-value, Cramér's V, and odds ratio (joined vs not) with 95% CI.")
rows = []
work = df.dropna(subset=["Joined"]).copy()
def or_ci(a, b, c, d):  # 2x2 with Haldane correction
    a, b, c, d = a + .5, b + .5, c + .5, d + .5
    orr = (a * d) / (b * c)
    se = math.sqrt(1/a + 1/b + 1/c + 1/d)
    lo, hi = math.exp(math.log(orr) - 1.96*se), math.exp(math.log(orr) + 1.96*se)
    return orr, lo, hi
for var in ["SOF", "Officer", "Combat", "CT_bin"]:
    if var == "CT_bin":
        work["CT_bin"] = (work["CT"] > 0).astype(int)
    ct = pd.crosstab(work[var], work["Joined"])
    if ct.shape == (2, 2):
        chi2, pval, dofree, _ = stats.chi2_contingency(ct, correction=False)
        # cells: predictor=1 & joined=1 etc.
        a = ct.loc[1, 1]; b = ct.loc[1, 0]; c = ct.loc[0, 1]; d = ct.loc[0, 0]
        orr, lo, hi = or_ci(a, b, c, d)
        _, fisher_p = stats.fisher_exact([[a, b], [c, d]])
        rows.append({"predictor": var, "chi2": round(chi2, 2), "p(chi2)": f"{pval:.1e}",
                     "p(Fisher)": f"{fisher_p:.1e}",
                     "V": round(cramers_v(chi2, ct.values.sum(), 2, 2), 2),
                     "OR(join)": round(orr, 2), "95% CI": f"{lo:.2f}-{hi:.2f}"})
tbl(pd.DataFrame(rows))

# multi-category predictors: Branch, Service
for var in ["Branch", "Service"]:
    ct = pd.crosstab(work[var], work["Joined"])
    chi2, pval, dofree, _ = stats.chi2_contingency(ct)
    h(f"B1b. {var} × Joined")
    tbl(ct.reset_index())
    p(f"chi2({dofree})={chi2:.1f}, p={pval:.1e}, "
      f"Cramér's V={cramers_v(chi2, ct.values.sum(), ct.shape[0], ct.shape[1]):.2f}")

# B2 — multivariate logistic regression predicting Joined
h("B2. Multivariable logistic regression (Firth-penalized) — predicting Joined")
p("Isolates the independent contribution of each factor (the bivariate "
  "comparisons are confounded: joiners are simultaneously older, more often "
  "officers, SOF and reserves). Reference: Service=Conscript, Branch=Military. "
  "**Firth penalization** is used because standard MLE does not converge here: "
  "Emergency Response Teams have 0 on-duty fatalities (complete separation — by "
  "definition they are local volunteers who joined), and Reserves are nearly "
  "separated. Firth yields finite, bias-reduced estimates.")
mdl_df = work.dropna(subset=["SOF", "Officer", "Combat", "Service", "Branch", "Age"]).copy()
mdl_df["Age_c"] = mdl_df["Age"] - mdl_df["Age"].mean()
# design matrix with explicit references (Service=Conscript, Branch=Military)
desg = pd.DataFrame({"Intercept": 1.0,
                     "SOF": mdl_df["SOF"].values,
                     "Officer": mdl_df["Officer"].values,
                     "Combat": mdl_df["Combat"].values,
                     "Age_c": mdl_df["Age_c"].values})
desg["Service:Professional"] = (mdl_df["Service"] == "Professional").astype(float).values
desg["Service:Reserves"] = (mdl_df["Service"] == "Reserves").astype(float).values
desg["Branch:Police"] = (mdl_df["Branch"] == "Police").astype(float).values
desg["Branch:ShinBet"] = (mdl_df["Branch"] == "Shin Bet").astype(float).values
desg["Branch:ERT"] = (mdl_df["Branch"] == "Emergency Response Team").astype(float).values
Xmat = desg.values.astype(float)
yvec = mdl_df["Joined"].values.astype(float)
beta, se = firth_logit(Xmat, yvec)
z = beta / se
pvals = 2 * (1 - stats.norm.cdf(np.abs(z)))
res = pd.DataFrame({
    "term": desg.columns,
    "OR": np.round(np.exp(beta), 2),
    "95% CI": [f"{math.exp(b-1.96*s):.2f}-{math.exp(b+1.96*s):.2f}" for b, s in zip(beta, se)],
    "p": [f"{x:.3f}" for x in pvals],
})
tbl(res)
p(f"n={len(yvec)} (Firth-penalized logistic regression).")

# B3 — time-to-death: Kruskal-Wallis + survival
h("B3. Time-to-death analysis")
p("ANOVA on hours-to-death is questionable (right-skewed, coarse, and the "
  "sample is itself a selected/censored set — survivors are absent). We "
  "report a non-parametric Kruskal-Wallis test plus Kaplan-Meier curves and "
  "a Cox proportional-hazards model. NOTE: every observation is an event "
  "(death); true right-censoring (survivors) is NOT in the data, so survival "
  "estimates describe the fallen only — interpret as time-to-falling among "
  "fatalities, not population hazard.")
tt = df.dropna(subset=["Time"]).copy()
# Kruskal-Wallis across branch and service and wave
for var in ["Wave", "Branch", "Service"]:
    groups = [g["Time"].values for _, g in tt.groupby(var) if len(g) >= 3]
    if len(groups) >= 2:
        H, pv = stats.kruskal(*groups)
        p(f"- Kruskal-Wallis, Time by {var}: H={H:.1f}, p={pv:.1e}")
# Mann-Whitney joined vs not
a = tt[tt["Joined"] == 1]["Time"]; b = tt[tt["Joined"] == 0]["Time"]
U, pv = stats.mannwhitneyu(a, b, alternative="two-sided")
p(f"- Mann-Whitney, Time joined({a.median():.0f}) vs on-duty({b.median():.0f}): "
  f"U={U:.0f}, p={pv:.1e}")

# Kaplan-Meier by wave (all events)
fig, ax = plt.subplots(figsize=(8, 4.8))
for i, (lab, sub) in enumerate(tt.groupby("Wave")):
    sf = SurvfuncRight(sub["Time"].values, np.ones(len(sub)))
    ax.step(sf.surv_times, sf.surv_prob, where="post", label=f"{lab} (n={len(sub)})",
            color=PALETTE[i])
ax.set_title("Kaplan-Meier: 'survival' until falling, by wave\n(events only — no survivors in data)")
ax.set_xlabel("Hours from attack start"); ax.set_ylabel("Proportion not yet fallen")
ax.legend()
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig6_km_by_wave.png")); plt.close(fig)

# Cox PH model
cox_df = tt.dropna(subset=["SOF", "Officer", "Joined", "Age"]).copy()
cox_df["Age_c"] = cox_df["Age"] - cox_df["Age"].mean()
try:
    status = np.ones(len(cox_df))
    cox = PHReg(cox_df["Time"].values,
                cox_df[["Joined", "SOF", "Officer", "Age_c"]].astype(float).values,
                status=status).fit()
    cres = pd.DataFrame({
        "term": ["Joined", "SOF", "Officer", "Age_c"],
        "HR": np.round(np.exp(cox.params), 2),
        "p": [f"{x:.3f}" for x in cox.pvalues],
    })
    h("B3b. Cox proportional-hazards (hazard of falling)")
    tbl(cres)
    p("HR<1 ⇒ lower instantaneous hazard ⇒ tended to fall later (lasted longer).")
except Exception as e:
    p(f"[Cox model failed: {e}]")

# B4 — SOF over-representation: bounding argument + sensitivity
h("B4. SOF over-representation — bounding argument with sensitivity")
p("No exact open-source count of total IDF SOF personnel exists (classified). "
  "Instead we bound it: fatalities show SOF share = "
  f"{(df['SOF']==1).mean()*100:.1f}% ({int((df['SOF']==1).sum())}/{N}). "
  "We compare against a *generous range* of assumed SOF shares of the 169,500 "
  "active IDF and report the rate ratio (RR). The conclusion is robust as long "
  "as true SOF share is a few percent.")
sof_fatal_share = (df["SOF"] == 1).mean()
rows = []
for assumed in [0.005, 0.01, 0.02, 0.03, 0.05]:
    rr = sof_fatal_share / assumed
    rows.append({"assumed SOF share of force": f"{assumed*100:.1f}%",
                 "implied SOF headcount /169,500": int(assumed*169500),
                 "SOF share of fatalities": f"{sof_fatal_share*100:.1f}%",
                 "rate ratio": round(rr, 1)})
tbl(pd.DataFrame(rows))
p("Even at a generous 5% assumed force share, SOF are over-represented among "
  "fatalities by a factor of ~3; at 1–2% the factor is ~8–16×.")

# ----------------------------------------------------------------------------
# write results.md
# ----------------------------------------------------------------------------
with open(os.path.join(OUT, "results.md"), "w", encoding="utf-8") as f:
    f.write("# ERC analysis results\n")
    f.write("\n".join(str(x) for x in md))
print("Done. Figures in", FIG)
print("Results in", os.path.join(OUT, "results.md"))
