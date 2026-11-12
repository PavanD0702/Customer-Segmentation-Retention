from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def segment_customers(rfm, n_clusters=4):
    """Cluster customers using scaled log-transformed RFM values."""
    rfm = rfm.copy()
    features = ["Recency", "Frequency", "Monetary"]
    X = np.log1p(rfm[features].clip(lower=0))
    X_scaled = StandardScaler().fit_transform(X)

    actual_clusters = min(n_clusters, len(rfm))
    if actual_clusters < 2:
        raise ValueError("At least two customers are needed for clustering.")

    model = KMeans(n_clusters=actual_clusters, random_state=42, n_init=10)
    rfm["Cluster"] = model.fit_predict(X_scaled)

    # Give cluster IDs understandable names using the cluster-level RFM averages.
    summary = rfm.groupby("Cluster")[features].mean()
    median_recency = summary["Recency"].median()
    median_frequency = summary["Frequency"].median()
    median_monetary = summary["Monetary"].median()

    best_cluster = summary[
        (summary["Recency"] <= median_recency)
        & (summary["Frequency"] >= median_frequency)
        & (summary["Monetary"] >= median_monetary)
    ]
    if best_cluster.empty:
        best_cluster_id = summary.sort_values(
            ["Recency", "Frequency", "Monetary"],
            ascending=[True, False, False]
        ).index[0]
    else:
        best_cluster_id = best_cluster.sort_values(
            ["Frequency", "Monetary"], ascending=False
        ).index[0]

    labels = {}
    for cluster_id, row in summary.iterrows():
        if cluster_id == best_cluster_id:
            labels[cluster_id] = "Best Customers"
        elif row["Recency"] > median_recency:
            labels[cluster_id] = "At Risk Customers"
        elif row["Frequency"] >= median_frequency:
            labels[cluster_id] = "Loyal Customers"
        else:
            labels[cluster_id] = "Regular Customers"

    rfm["Segment"] = rfm["Cluster"].map(labels)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output = PROCESSED_DIR / "customer_segments.csv"
    rfm.to_csv(output, index=False)
    print(f"Customer segments saved: {output}")
    print(rfm["Segment"].value_counts())
    return rfm


if __name__ == "__main__":
    from src.data_cleaning import clean_data
    from src.rfm_analysis import calculate_rfm
    segment_customers(calculate_rfm(clean_data()))
