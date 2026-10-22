"""Modul preprocessing: deteksi outlier IQR, korelasi heatmap, dan scaling."""
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from src.config import config

logger = logging.getLogger(__name__)


def detect_outliers_iqr(X: pd.DataFrame) -> pd.Series:
    """Menandai outlier menggunakan metode IQR tanpa menghapus data."""
    X_num = X.select_dtypes(include=[np.number])
    q1 = X_num.quantile(0.25)
    q3 = X_num.quantile(0.75)
    iqr = q3 - q1
    mult = config["preprocessing"]["iqr_multiplier"]
    lower = q1 - mult * iqr
    upper = q3 + mult * iqr
    outlier_mask = ((X_num < lower) | (X_num > upper)).any(axis=1)
    return outlier_mask


def generate_correlation_heatmap(X: pd.DataFrame, out_path: Path | str) -> None:
    """Membuat dan menyimpan heatmap korelasi 6 fitur."""
    plt.figure(figsize=(8, 6))
    corr = X.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
    plt.title("Heatmap Korelasi 6 Fitur Model")
    plt.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=300)
    plt.close()
    logger.info(f"Heatmap korelasi tersimpan di {out_path}")


def scale_features(X: pd.DataFrame) -> tuple[np.ndarray, object]:
    """Melakukan scaling fitur menggunakan StandardScaler atau MinMaxScaler sesuai config."""
    scaler_type = config["preprocessing"]["scaler"]
    if scaler_type == "minmax":
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    
    if "kode_siswa" in X.columns:
        X = X.drop(columns=["kode_siswa"])
    X_num = X.select_dtypes(include=[np.number])
    X_scaled = scaler.fit_transform(X_num)
    logger.info(f"Scaling fitur selesai menggunakan {scaler_type}.")
    return X_scaled, scaler


def preprocess(X: pd.DataFrame):
    return X, detect_outliers_iqr(X)
