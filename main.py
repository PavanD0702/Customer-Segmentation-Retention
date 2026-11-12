from src.data_cleaning import clean_data
from src.rfm_analysis import calculate_rfm
from src.customer_segmentation import segment_customers
from src.retention_analysis import retention_analysis


def main():
    print("=" * 60)
    print("CUSTOMER SEGMENTATION AND RETENTION ANALYSIS")
    print("=" * 60)

    transactions = clean_data()
    rfm = calculate_rfm(transactions)
    segments = segment_customers(rfm)
    retention = retention_analysis(transactions)

    print("\nAll analysis completed successfully.")
    print("Processed files are available in: data/processed/")
    print("Start the dashboard with: streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()
