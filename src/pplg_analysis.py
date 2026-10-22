"""Modul analisis tambahan PPLG: statistik deskriptif dan boxplot per cluster (tanpa uji signifikansi)."""
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import config

logger = logging.getLogger(__name__)


def analyze_pplg_scores(df_siswa: pd.DataFrame, labels) -> pd.DataFrame:
    """Menghitung statistik deskriptif (mean, sd, n) skor_PPLG per cluster dan membuat boxplot."""
    df = df_siswa.copy()
    df["cluster"] = labels

    if "skor_PPLG" not in df.columns:
        df["skor_PPLG"] = 0.0

    stats = df.groupby("cluster")["skor_PPLG"].agg(["count", "mean", "std"]).reset_index()
    stats.rename(columns={"count": "n", "mean": "mean_skor_pplg", "std": "sd_skor_pplg"}, inplace=True)

    plt.figure(figsize=(8, 5))
    sns.boxplot(x="cluster", y="skor_PPLG", data=df)
    plt.title("Distribusi Skor PPLG Berdasarkan Cluster (Analisis Tambahan)")
    plt.xlabel("Cluster")
    plt.ylabel("Skor PPLG")
    plt.tight_layout()

    out_path = Path(config["paths"]["figures_dir"]) / "pplg_boxplot.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()

    logger.info("Analisis tambahan PPLG selesai.")
    return stats
