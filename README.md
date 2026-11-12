# Customer Segmentation and Retention Analysis

## Project overview
This project analyzes the UCI Online Retail transaction dataset. It cleans transaction data, calculates customer Recency, Frequency, and Monetary (RFM) metrics, groups customers with K-Means clustering, and measures repeat-purchase retention using monthly cohorts.

## Tools
- Python, Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn (K-Means)
- Streamlit
- VS Code

## Dataset setup
1. Download the **Online Retail** dataset from the UCI Machine Learning Repository:
   https://archive.ics.uci.edu/dataset/352/online+retail
2. Extract the download if it is a ZIP file.
3. Place `Online Retail.xlsx` in `data/raw/`.
4. Do not rename the file unless you also update `RAW_FILE` in `src/data_cleaning.py`.

The dataset is not included in this project ZIP. Download it from UCI and add it locally.

## Setup in Windows / VS Code
Open this project folder in VS Code, then open Terminal.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Check that the Excel file can be read:

```powershell
python test_data.py
```

Run all analysis:

```powershell
python main.py
```

Run the dashboard from the project root:

```powershell
streamlit run dashboard/app.py
```

## Output files
Generated CSV files are saved in `data/processed/`:
- `cleaned_transactions.csv`
- `rfm_analysis.csv`
- `customer_segments.csv`
- `retention_analysis.csv`

## Methodology
- Data cleaning: remove missing customer IDs, duplicates, cancelled invoices, and non-positive quantities/prices.
- RFM: recency is days since the customer's last purchase; frequency is the number of distinct invoices; monetary is total transaction value.
- Segmentation: K-Means on log-transformed and standardized RFM values.
- Retention: monthly cohorts based on each customer's first purchase month.

## Important interpretation note
The customer segment names are assigned using simple rules based on cluster-level RFM averages. “At Risk Customers” is an analytical indicator, not a supervised model that predicts future churn. Cohort retention describes observed repeat purchasing, not proof of why customers returned or left.

## Dataset citation
Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33
