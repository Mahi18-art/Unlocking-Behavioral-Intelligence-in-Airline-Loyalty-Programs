# Unlocking Behavioral Intelligence in Airline Loyalty Programs

Behavioral churn prediction and a retention action planner for 16,737 Canadian
airline loyalty members (2017–2018), delivered as an interactive Streamlit
dashboard.

## What's in here

| Path | Purpose |
|---|---|
| `app.py` | Streamlit dashboard (segments, churn risk, retention playbook, customer lookup) |
| `airline_loyalty_final.ipynb` | Full analysis: cleaning, feature engineering, segmentation, churn model, exports |
| `plots/` | Static charts from the analysis |
| `data/` | Holds `Customer_Retention_Action_Plan.csv` (see `data/README.md`) |
| `requirements.txt` | Python dependencies for deployment |

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app needs `data/Customer_Retention_Action_Plan.csv`. If it is missing, the
app shows instructions instead of crashing — see `data/README.md` to generate it.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (including `data/Customer_Retention_Action_Plan.csv`).
2. Go to https://share.streamlit.io → **New app**.
3. Pick this repository, branch `main`, and set **Main file path** to `app.py`.
4. Deploy. Streamlit installs `requirements.txt` automatically.
