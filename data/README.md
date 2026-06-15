# data/

The Streamlit app (`app.py`) reads **one** file from this folder:

```
data/Customer_Retention_Action_Plan.csv
```

This file is **not** generated automatically on deploy — you must produce it and
commit it to the repo, because Streamlit Community Cloud only has access to what
is in the GitHub repository.

## How to generate it

1. Place the three raw Kaggle source files in this folder:
   - `Customer Flight Activity.csv`
   - `Customer Loyalty History.csv`
   - `Calendar.csv`
2. Run `airline_loyalty_final.ipynb` top to bottom. Its final cells export
   `data/Customer_Retention_Action_Plan.csv` (one row per loyalty member).
3. Commit **only** `Customer_Retention_Action_Plan.csv` (the raw and intermediate
   files are git-ignored to keep the repo small).

## Required columns

`app.py` expects these columns: `Loyalty Number`, `Segment_Name`,
`Churn_Risk_Tier` (values `Low Risk` / `Medium Risk` / `High Risk`),
`Churn_Probability`, `CLV`, `Action`, `Priority`, `Budget`, plus the profile
fields shown in the customer lookup (`Loyalty Card`, `Gender`, `Education`,
`Marital Status`, `Province`, `Salary`, `Total_Flights_2Yr`,
`Active_Months_Ratio`, `Months_Since_Last_Flight`, `Churn_Label`).
