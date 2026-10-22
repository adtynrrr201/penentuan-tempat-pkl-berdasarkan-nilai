"""Modul K-Means: k=2..4, metrik evaluasi, elbow plot, dan penanda cluster < 3 siswa."""
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score

from src.config import config

logger = logging.getLogger(__name__)


def run_kmeans_pipeline(X_scaled: np.ndarray) -> dict:
    """Menjalankan K-Means untuk k = 2..4, menghitung silhouette, DBI, inertia, dan elbow plot."""
    k_values = config["kmeans"]["k_values"]
    n_init = config["kmeans"]["n_init"]
    random_state = config["kmeans"]["random_state"]

    results = {}
    inertias = []
    silhouettes = []

    for k in k_values:
        kmeans = KMeans(n_clusters=k, n_init=n_init, random_state=random_state)
        labels = kmeans.fit_predict(X_scaled)
        
        inertia = kmeans.inertia_
        inertias.append(inertia)
        
        sil = silhouette_score(X_scaled, labels)
        silhouettes.append(sil)
        
        dbi = davies_bouldin_score(X_scaled, labels)
        
        # Cek cluster < 3 siswa
        unique, counts = np.unique(labels, return_counts=True)
        small_clusters = [int(u) for u, c in zip(unique, counts) if c < 3]

        results[k] = {
            "labels": labels,
            "inertia": inertia,
            "silhouette": sil,
            "davies_bouldin": dbi,
            "cluster_counts": dict(zip(unique.tolist(), counts.tolist())),
            "small_clusters_warning": bool(small_clusters),
        }

    # Plot Elbow
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(k_values, inertias, 'bo-', label="Inertia")
    ax1.set_xlabel("Jumlah Cluster (k)")
    ax1.set_ylabel("Inertia", color='b')
    
    ax2 = ax1.twinx()
    ax2.plot(k_values, silhouettes, 'ro--', label="Silhouette Score")
    ax2.set_ylabel("Silhouette Score", color='r')
    
    plt.title("Elbow Method & Silhouette untuk K-Means")
    plt.tight_layout()
    
    out_path = Path(config["paths"]["figures_dir"]) / "kmeans_elbow.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()

    logger.info("Pipeline K-Means selesai dijalankan.")
    return results
