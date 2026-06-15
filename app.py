from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Loyalty Dashboard", layout="wide")

# Resolve the data path relative to this file so it works locally and on
# Streamlit Community Cloud regardless of the process working directory.
DATA_PATH = Path(__file__).parent / "data" / "Customer_Retention_Action_Plan.csv"


@st.cache_data
def load_data(path):
    return pd.read_csv(path)


if not DATA_PATH.exists():
    st.error(
        "Required data file not found: `data/Customer_Retention_Action_Plan.csv`.\n\n"
        "Generate it by running `airline_loyalty_final.ipynb` (it exports this file "
        "to the `data/` folder) and commit it to the repository so the deployed app "
        "can read it."
    )
    st.stop()

df = load_data(DATA_PATH)

# Sidebar filters
st.sidebar.title("Filters")
seg = st.sidebar.multiselect("Segment",    df["Segment_Name"].unique(
),    default=list(df["Segment_Name"].unique()))
risk = st.sidebar.multiselect("Churn Risk", df["Churn_Risk_Tier"].unique(
), default=list(df["Churn_Risk_Tier"].unique()))
df_f = df[df["Segment_Name"].isin(seg) & df["Churn_Risk_Tier"].isin(risk)]

# Title
st.title("Airline Loyalty Intelligence Dashboard")
st.caption("Behavioural churn prediction and retention planner — 16,737 Canadian loyalty members (2017–2018)")
st.divider()

# KPI cards
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Members",  f"{len(df_f):,}")
k2.metric("High Risk",
          f"{(df_f['Churn_Risk_Tier'] == 'High Risk').sum():,}")
k3.metric("Avg Churn Prob", f"{df_f['Churn_Probability'].mean()*100:.1f}%")
k4.metric("CLV at Risk",
          f"${df_f[df_f['Churn_Risk_Tier'] == 'High Risk']['CLV'].sum()/1e6:.1f}M")
st.divider()

# Row 1 — Segment overview
st.subheader("Segment Overview")
c1, c2, c3 = st.columns(3)

with c1:
    fig = px.pie(df_f, names="Segment_Name", hole=0.4,
                 title="Customer Distribution")
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    seg_churn = df_f.groupby("Segment_Name")[
        "Churn_Probability"].mean().reset_index()
    fig = px.bar(seg_churn, x="Segment_Name", y="Churn_Probability",
                 title="Avg Churn Probability by Segment",
                 color="Segment_Name", text_auto=".1%")
    fig.update_layout(showlegend=False, yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with c3:
    seg_clv = df_f.groupby("Segment_Name")["CLV"].mean().reset_index()
    fig = px.bar(seg_clv, x="Segment_Name", y="CLV",
                 title="Avg CLV by Segment ($)",
                 color="Segment_Name", text_auto=",.0f")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Row 2 — Risk matrix + CLV at risk
st.subheader("Churn Risk Intelligence")
c1, c2 = st.columns(2)

with c1:
    matrix = pd.crosstab(df_f["Segment_Name"], df_f["Churn_Risk_Tier"])
    for col in ["Low Risk", "Medium Risk", "High Risk"]:
        if col not in matrix.columns:
            matrix[col] = 0
    matrix = matrix[["Low Risk", "Medium Risk", "High Risk"]]
    fig = px.imshow(matrix, text_auto=True, color_continuous_scale="YlOrRd",
                    title="Segment x Churn Risk Matrix (Customer Counts)", aspect="auto")
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    clv_risk = (df_f[df_f["Churn_Risk_Tier"] == "High Risk"]
                .groupby("Segment_Name")["CLV"].sum().reset_index())
    clv_risk.columns = ["Segment", "CLV at Risk"]
    fig = px.bar(clv_risk, x="Segment", y="CLV at Risk",
                 title="Total CLV at Risk — High Risk Customers ($)",
                 color="Segment", text_auto=",.0f")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Row 3 — Retention playbook
st.subheader("Retention Action Playbook")
playbook = (df_f[["Segment_Name", "Churn_Risk_Tier", "Action", "Priority", "Budget"]]
            .drop_duplicates(subset=["Segment_Name", "Churn_Risk_Tier"])
            .sort_values(["Segment_Name", "Churn_Risk_Tier"])
            .reset_index(drop=True))
st.dataframe(playbook, use_container_width=True, hide_index=True)
st.divider()

# Row 4 — Customer lookup
st.subheader("Customer Lookup")
search_id = st.number_input("Enter Loyalty Number", min_value=0, step=1)
if st.button("Search") and search_id > 0:
    row = df[df["Loyalty Number"] == search_id]
    if row.empty:
        st.error(f"No customer found with Loyalty Number {search_id}")
    else:
        row = row.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Segment",    row["Segment_Name"])
        c2.metric("Churn Risk", row["Churn_Risk_Tier"])
        c3.metric("Churn Prob", f"{row['Churn_Probability']*100:.1f}%")
        c4.metric("CLV",        f"${row['CLV']:,.0f}")
        st.write(f"**Recommended Action:** {row['Action']}")
        st.write(
            f"**Priority:** {row['Priority']}  |  **Budget:** {row['Budget']}")

        with st.expander("Full Customer Profile"):
            show_cols = ["Loyalty Number", "Loyalty Card", "Gender", "Education",
                         "Marital Status", "Province", "Salary", "CLV",
                         "Total_Flights_2Yr", "Active_Months_Ratio",
                         "Months_Since_Last_Flight", "Segment_Name",
                         "Churn_Risk_Tier", "Churn_Probability", "Churn_Label"]
            show_cols = [c for c in show_cols if c in df.columns]
            st.dataframe(row[show_cols].to_frame().rename(
                columns={row.name: "Value"}))

st.divider()

# Row 5 — Full customer table
st.subheader("All Customers")
show_cols = ["Loyalty Number", "Segment_Name", "Churn_Risk_Tier",
             "Churn_Probability", "CLV", "Action", "Priority"]
show_cols = [c for c in show_cols if c in df_f.columns]
st.dataframe(df_f[show_cols].sort_values("Churn_Probability", ascending=False),
             use_container_width=True, hide_index=True)
