"""Modul kesepakatan antarmetode: ARI, NMI, dan tabel kontingensi (noise diperlakukan sebagai label sendiri)."""
import logging
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

from src.config import config

logger = logging.getLogger(__name__)


def compute_agreement(labels_a: np.ndarray, labels_b: np.ndarray) -> dict:
    """Menghitung ARI dan NMI berpasangan antara dua metode clustering."""
    ari = adjusted_rand_score(labels_a, labels_b)
    nmi = normalized_mutual_info_score(labels_a, labels_b)

    # Tabel kontingensi
    contingency = pd.crosstab(
        pd.Series(labels_a, name="Metode_A"),
        pd.Series(labels_b, name="Metode_B"),
    )

    return {
        "ARI": float(ari),
        "NMI": float(nmi),
        "contingency_table": contingency,
    }
