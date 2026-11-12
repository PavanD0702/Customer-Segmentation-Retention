from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "processed"

st.set_page_config(page_title="Customer Analytics", page_icon="📊", layout="wide")
st.title("Customer Segmentation and Retention Analysis")
st.caption("Explore customer purchasing patterns using RFM, K-Means clustering, and cohort retention.")

segments_file = DATA_DIR / "customer_segments.csv"
retention_file = DATA_DIR / "retention_analysis.csv"

if not segments_file.exists() or not retention_file.exists():
    st.warning("Analysis files are missing. First run `python main.py` from the project root folder.")
    st.stop()

rfm = pd.read_csv(segments_file)
retention = pd.read_csv(retention_file, index_col=0)

c1, c2, c3 = st.columns(3)
c1.metric("Customers", f"{rfm['CustomerID'].nunique():,}")
c2.metric("Total customer revenue", f"{rfm['Monetary'].sum():,.2f}")
c3.metric("Segments", f"{rfm['Segment'].nunique()}")

st.subheader("Customer segment distribution")
counts = rfm["Segment"].value_counts()
fig, ax = plt.subplots(figsize=(9, 4))
counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Segment")
ax.set_ylabel("Number of customers")
ax.tick_params(axis="x", rotation=20)
st.pyplot(fig)
plt.close(fig)

st.subheader("Customer retention by cohort (%)")
retention.index = retention.index.astype(str)
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(retention, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_xlabel("Months since first purchase")
ax.set_ylabel("First purchase month")
st.pyplot(fig)
plt.close(fig)

st.subheader("Customer details")
selected = st.multiselect(
    "Filter customer segments",
    sorted(rfm["Segment"].dropna().unique()),
    default=sorted(rfm["Segment"].dropna().unique())
)
st.dataframe(
    rfm[rfm["Segment"].isin(selected)].sort_values("Monetary", ascending=False),
    use_container_width=True
)

st.info("At-risk labels are rule-based indicators derived from RFM cluster averages; they are not a trained future-churn prediction.")
