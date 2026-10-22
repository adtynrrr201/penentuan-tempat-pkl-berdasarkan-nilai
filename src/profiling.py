"""Modul profil bidang: rata-rata fitur per cluster, label bidang, dan deteksi ketidakselarasan."""
import logging
import numpy as np
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)


def profile_clusters(df: pd.DataFrame, labels: np.ndarray, feature_cols: list[str] | None = None) -> pd.DataFrame:
    """Hitung mean per cluster (exclude noise -1). Return DataFrame index=cluster."""
    cols = feature_cols or [
        "komp_jaringan",
        "komp_admin",
        "komp_support",
        "minat_jaringan",
        "minat_admin",
        "minat_support",
    ]
    df2 = df.copy()
    df2["Cluster"] = labels
    clustered = df2[df2["Cluster"] != -1]
    if clustered.empty:
        return pd.DataFrame(columns=cols + ["Jumlah_Anggota"])
    profil = clustered.groupby("Cluster")[cols].mean().round(2)
    counts = clustered.groupby("Cluster").size().rename("Jumlah_Anggota")
    profil = profil.join(counts)
    profil.index.name = "Cluster"
    return profil


def detect_noise(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """Return subset siswa dengan label -1."""
    return df[labels == -1].copy()


def profile_and_label_clusters(df_siswa: pd.DataFrame, labels: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Membuat profil rata-rata tiap fitur per cluster, menetapkan label bidang, dan kategori tidak selaras."""
    profile_df = profile_clusters(df_siswa, labels)
    
    df = df_siswa.copy()
    df["cluster"] = labels

    student_labels = []
    for idx, row in df.iterrows():
        cl = row["cluster"]
        if cl == -1:
            student_labels.append("Noise / Outlier")
        else:
            comp_scores = {
                "jaringan_dasar": row["komp_jaringan"],
                "administrasi_jaringan": row["komp_admin"],
                "technical_support": row["komp_support"],
            }
            int_scores = {
                "jaringan_dasar": row["minat_jaringan"],
                "administrasi_jaringan": row["minat_admin"],
                "minat_support": row["minat_support"],
            }
            s_comp = max(comp_scores, key=comp_scores.get)
            s_int = max(int_scores, key=int_scores.get)
            
            status = "Selaras" if s_comp == s_int else "Tidak Selaras"
            student_labels.append(f"{s_comp} ({status})")

    df["kecenderungan_bidang"] = student_labels
    logger.info("Profiling dan pelabelan cluster selesai.")
    return profile_df, df
