"""Modul kestabilan: K-Means pada 100 seed, subsampling 80%, dan variasi eps DBSCAN."""
import logging
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import adjusted_rand_score

from src.config import config

logger = logging.getLogger(__name__)


def evaluate_kmeans_stability(X_scaled: np.ndarray, base_labels: np.ndarray) -> dict:
    """Menguji kestabilan K-Means pada 100 seed terhadap label acuan."""
    seeds = config["stability"]["kmeans_seeds"]
    k = len(np.unique(base_labels))
    aris = []

    for seed in range(seeds):
        km = KMeans(n_clusters=k, n_init=10, random_state=seed)
        labels = km.fit_predict(X_scaled)
        ari = adjusted_rand_score(base_labels, labels)
        aris.append(ari)

    return {
        "mean_ari": float(np.mean(aris)),
        "std_ari": float(np.std(aris)),
        "min_ari": float(np.min(aris)),
        "max_ari": float(np.max(aris)),
    }


def evaluate_subsample_stability(X_scaled: np.ndarray, k: int) -> dict:
    """Menguji kestabilan subsampling 80% berulang (K-Means)."""
    ratio = config["stability"]["subsample_ratio"]
    iters = config["stability"]["subsample_iterations"]
    n_samples = len(X_scaled)
    sub_size = int(n_samples * ratio)
    
    base_km = KMeans(n_clusters=k, n_init=10, random_state=config["project"]["seed"])
    base_labels = base_km.fit_predict(X_scaled)

    aris = []
    for i in range(iters):
        np.random.seed(i)
        idx = np.random.choice(n_samples, sub_size, replace=False)
        sub_X = X_scaled[idx]
        
        km = KMeans(n_clusters=k, n_init=10, random_state=i)
        sub_labels = km.fit_predict(sub_X)
        
        ari = adjusted_rand_score(base_labels[idx], sub_labels)
        aris.append(ari)

    return {
        "subsample_mean_ari": float(np.mean(aris)),
        "subsample_std_ari": float(np.std(aris)),
    }
