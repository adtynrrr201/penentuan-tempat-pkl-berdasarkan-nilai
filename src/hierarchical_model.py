"""Modul Hierarchical (Ward): dendrogram, cophenetic correlation, dan pemotongan cluster."""
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet, dendrogram, fcluster, linkage
from scipy.spatial.distance import pdist
from sklearn.metrics import silhouette_score

from src.config import config

logger = logging.getLogger(__name__)


def run_hierarchical_pipeline(X_scaled: np.ndarray, k_target: int = 3) -> dict:
    """Menjalankan Hierarchical Clustering (Ward + Euclidean), dendrogram, dan cophenetic correlation."""
    method = config["hierarchical"]["linkage_method"]
    metric = config["hierarchical"]["metric"]

    # Hitung linkage matrix
    Z = linkage(X_scaled, method=method, metric=metric)

    # Cophenetic correlation
    c, coph_dist = cophenet(Z, pdist(X_scaled, metric=metric))

    # Potong di k_target
    labels = fcluster(Z, t=k_target, criterion="maxclust") - 1  # 0-indexed

    sil = silhouette_score(X_scaled, labels) if len(np.unique(labels)) > 1 else 0.0

    # Dendrogram plot
    plt.figure(figsize=(10, 6))
    dendrogram(Z)
    plt.title(f"Dendrogram Hierarchical Clustering (Ward, Cophenet c={c:.3f})")
    plt.xlabel("Index Siswa")
    plt.ylabel("Jarak Euclidean")
    plt.tight_layout()

    out_path = Path(config["paths"]["figures_dir"]) / "hierarchical_dendrogram.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()

    logger.info(f"Hierarchical Ward selesai. Cophenetic c = {c:.4f}")
    return {
        "linkage_matrix": Z,
        "cophenetic_correlation": float(c),
        "labels": labels,
        "silhouette": float(sil),
    }
