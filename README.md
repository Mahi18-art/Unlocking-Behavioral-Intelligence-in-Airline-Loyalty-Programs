# Unlocking Behavioral Intelligence in Airline Loyalty Programs

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://4tmgueytklxvnjbes5qhga.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B.svg)](https://streamlit.io/)

Behavioral **churn prediction** and a **retention action planner** for **16,737**
Canadian airline loyalty members (Jan 2017 – Dec 2018), delivered as an
interactive Streamlit dashboard.

### Live app: **https://4tmgueytklxvnjbes5qhga.streamlit.app/**

---

## The idea

Loyalty programs are usually managed around points and rewards. The blind spot:
a member can look healthy on paper — still enrolled, high historical CLV — while
having quietly **stopped flying months ago**. By the time a formal cancellation
lands, the relationship is already dead.

This project reframes the problem around three questions:

1. **Churn (early warning)** — who is *behaviorally* disengaging now, before they cancel?
2. **Value & segmentation** — who is genuinely valuable *going forward*, not just historically?
3. **Retention (action)** — for each customer type, what specific intervention should run tomorrow?

> **Headline finding:** CLV does *not* tell the full story. The **Dormant**
> segment (already 100% churned) carries the **highest average CLV (~$7,782)** —
> a manager ranking by CLV would put already-departed members at the top.
> Historical CLV is a rear-view mirror; forward value needs behavioral signals.

---

## The dashboard

The Streamlit app (`app.py`) turns the model output into an operational tool:

- **KPI cards** — total members, high-risk count, average churn probability, and total CLV at risk
- **Segment overview** — customer distribution, average churn probability, and average CLV per segment
- **Churn risk intelligence** — Segment × Risk matrix and total CLV at risk among high-risk members
- **Retention action playbook** — the 12-cell (Segment × Risk) intervention matrix with priority and budget
- **Customer lookup** — search any loyalty number for their segment, risk, churn probability, recommended action, and full profile
- **Filterable table** — every member, sorted by churn probability, filtered by segment and risk in the sidebar

---

## The analysis (`airline_loyalty_final.ipynb`)

| Stage | What happens |
|---|---|
| **Data quality** | Documented cleaning of 392,936 flight rows → 389,065 (deduped/summed); missing-salary and missing-cancellation handled as informative, not random |
| **Feature engineering** | 389,065 monthly rows → one behavioral signature per member (recency, active-months ratio, max inactivity streak, redemption rate, seasonality) |
| **Churn label** | Behavioral churn = ≥ 6 consecutive months of zero flights *and* zero redemptions → **14.7%** of members |
| **Leakage control** | Strict time split — learn from months 1–18, label from months 19–24 |
| **Segmentation** | K-Means (K=4) on pure behavioral features → Champions / Loyalists / At-Risk / Dormant |
| **Churn model** | Gradient Boosting — **ROC-AUC 0.957**, **86% recall** on churners; explained with SHAP |
| **Output** | Per-member action plan exported to `data/Customer_Retention_Action_Plan.csv` |

### Key numbers

| Segment | Size | Share | Avg CLV | Behavioral churn |
|---|---|---|---|---|
| Champions | 8,201 | 49.0% | $7,595 | 1% |
| Loyalists | 3,417 | 20.4% | $7,473 | 6% |
| At-Risk   | 3,217 | 19.2% | $7,418 | 8% |
| Dormant   | 1,902 | 11.4% | $7,782 | 100% |

Risk tiers across the base: **12,590 Low · 1,705 Medium · 2,442 High** —
the high-risk population alone represents **~$18.6M of CLV at risk**.

---

## Run locally

```bash
git clone https://github.com/Mahi18-art/Unlocking-Behavioral-Intelligence-in-Airline-Loyalty-Programs.git
cd Unlocking-Behavioral-Intelligence-in-Airline-Loyalty-Programs

pip install -r requirements.txt
streamlit run app.py
```

The app reads `data/Customer_Retention_Action_Plan.csv` (already committed). If it
is ever missing, the app shows generation instructions instead of crashing — see
[`data/README.md`](data/README.md).

---

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (including `data/Customer_Retention_Action_Plan.csv`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Repository: this repo · Branch: `main` · **Main file path:** `app.py`.
4. **Deploy** — dependencies install automatically from `requirements.txt`.

> Dependencies use lower-bound versions (`streamlit>=1.58`, `pandas>=3.0`,
> `plotly>=5.24`) so they resolve to wheels compatible with the Python version on
> Streamlit Cloud.

---

## Project structure

```
.
├── app.py                       # Streamlit dashboard
├── airline_loyalty_final.ipynb  # Full analysis notebook (cleaning → model → export)
├── requirements.txt             # Deployment dependencies
├── plots/                       # Static charts from the analysis
├── data/
│   ├── Customer_Retention_Action_Plan.csv  # Per-member output (read by app.py)
│   └── README.md                # How to regenerate the data
└── README.md
```

---

## Tech stack

`Python` · `pandas` · `scikit-learn` · `XGBoost` · `SHAP` · `Plotly` · `Streamlit`
