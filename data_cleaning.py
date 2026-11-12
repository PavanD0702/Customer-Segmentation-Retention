from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_data():
    """Read the original Excel file, clean transactions, and save a CSV."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {RAW_FILE}\n"
            "Download Online Retail.xlsx and place it in data/raw/."
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(RAW_FILE)
    print(f"Original dataset shape: {df.shape}")

    df = df.dropna(subset=["CustomerID"]).drop_duplicates()
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df[~df["InvoiceNo"].str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].copy()
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    output = PROCESSED_DIR / "cleaned_transactions.csv"
    df.to_csv(output, index=False)
    print(f"Cleaned dataset shape: {df.shape}")
    print(f"Saved: {output}")
    return df


if __name__ == "__main__":
    clean_data()
