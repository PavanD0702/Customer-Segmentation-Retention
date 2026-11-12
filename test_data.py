from pathlib import Path
import pandas as pd

file_path = Path("data/raw/Online Retail.xlsx")
if not file_path.exists():
    raise FileNotFoundError(
        f"Cannot find {file_path.resolve()}. Put Online Retail.xlsx in data/raw/."
    )

df = pd.read_excel(file_path)
print("Dataset loaded successfully!")
print(df.head())
print("Rows and columns:", df.shape)
print("Columns:", df.columns.tolist())
