"""Modul DBSCAN: k-distance graph, grid search eps, min_samples, dan evaluasi noise."""
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

from src.config import config

logger = logging.getLogger(__name__)


def generate_k_distance_graph(X_scaled: np.ndarray, min_samples: int) -> float:
    """Membuat grafik k-distance untuk membantu penentuan eps."""
    k = min_samples
    nbrs = NearestNeighbors(n_neighbors=k).fit(X_scaled)
    distances, _ = nbrs.kneighbors(X_scaled)
    k_distances = np.sort(distances[:, k - 1])

    plt.figure(figsize=(8, 5))
    plt.plot(k_distances)
    plt.title(f"Grafik K-Distance (k={k})")
    plt.xlabel("Poin (diurutkan berdasarkan jarak)")
    plt.ylabel(f"Jarak ke-{k} Neighbor")
    plt.tight_layout()

    out_path = Path(config["paths"]["figures_dir"]) / "dbscan_k_distance.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()

    # Estimasi kasar titik elbow (misal persentil 90)
    estimated_eps = float(np.percentile(k_distances, 90))
    return estimated_eps


def run_dbscan_grid_search(X_scaled: np.ndarray) -> pd.DataFrame:
    """Melakukan grid search sederhana untuk kombinasi eps dan min_samples pada DBSCAN."""
    min_samples_list = config["dbscan"]["min_samples_list"]
    steps = config["dbscan"]["eps_grid_steps"]

    # Cari rentang eps dari jarak min_samples
    nbrs = NearestNeighbors(n_neighbors=max(min_samples_list)).fit(X_scaled)
    distances, _ = nbrs.kneighbors(X_scaled)
    max_dist = np.max(distances)
    eps_grid = np.linspace(0.2, max_dist, steps)

    records = []

    for ms in min_samples_list:
        for eps in eps_grid:
            db = DBSCAN(eps=eps, min_samples=ms)
            labels = db.fit_predict(X_scaled)
            
            unique, counts = np.unique(labels, return_counts=True)
            counts_map = dict(zip(unique, counts))
            
            n_noise = int(counts_map.get(-1, 0))
            n_clusters = int(len(unique) - (1 if -1 in unique else 0))
            pct_noise = (n_noise / len(X_scaled)) * 100

            # Silhouette hanya pada non-noise jika cluster >= 2
            sil = float("nan")
            non_noise_mask = labels != -1
            if n_clusters >= 2 and non_noise_mask.sum() >= 2:
                try:
                    sil = silhouette_score(X_scaled[non_noise_mask], labels[non_noise_mask])
                except Exception:
                    pass

            records.append({
                "eps": float(eps),
                "min_samples": int(ms),
                "n_clusters": n_clusters,
                "n_noise": n_noise,
                "pct_noise": pct_noise,
                "silhouette_non_noise": sil,
            })

    df_grid = pd.DataFrame(records)
    logger.info("Grid search DBSCAN selesai.")
    return df_grid
