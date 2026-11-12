from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def retention_analysis(df):
    """Build a monthly cohort retention table based on each customer's first order."""
    df = df.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")
    df["CohortMonth"] = (
        df.groupby("CustomerID")["InvoiceDate"]
        .transform("min")
        .dt.to_period("M")
    )

    invoice_month_num = df["InvoiceMonth"].dt.year * 12 + df["InvoiceMonth"].dt.month
    cohort_month_num = df["CohortMonth"].dt.year * 12 + df["CohortMonth"].dt.month
    df["CohortIndex"] = (invoice_month_num - cohort_month_num + 1).astype(int)

    cohort_data = df.groupby(
        ["CohortMonth", "CohortIndex"]
    )["CustomerID"].nunique().reset_index(name="Customers")

    cohort_counts = cohort_data.pivot(
        index="CohortMonth", columns="CohortIndex", values="Customers"
    )
    retention = cohort_counts.divide(cohort_counts.iloc[:, 0], axis=0) * 100

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output = PROCESSED_DIR / "retention_analysis.csv"
    retention.to_csv(output)
    print(f"Retention table saved: {output}")
    return retention


if __name__ == "__main__":
    from src.data_cleaning import clean_data
    retention_analysis(clean_data())
