from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def calculate_rfm(df):
    """Calculate Recency, Frequency, and Monetary value per customer."""
    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda dates: (snapshot_date - dates.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("TotalPrice", "sum"),
    ).reset_index()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output = PROCESSED_DIR / "rfm_analysis.csv"
    rfm.to_csv(output, index=False)
    print(f"RFM results saved: {output}")
    return rfm


if __name__ == "__main__":
    from src.data_cleaning import clean_data
    calculate_rfm(clean_data())
