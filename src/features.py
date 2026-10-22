"""Modul fitur: pemetaan mapel dan kuesioner ke 6 fitur model utama."""
import logging
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)


def extract_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Mengekstrak fitur utama dan mengubah tipe data menjadi numerik."""
    comp_map = config["mapping"]["competency"]
    int_map = config["mapping"]["interest"]
    
    for col in df.columns:
        if col != "kode_siswa":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    features_df = pd.DataFrame()
    features_df["kode_siswa"] = df["kode_siswa"]

    model_feature_cols = [
        "komp_jaringan",
        "komp_admin",
        "komp_support",
        "minat_jaringan",
        "minat_admin",
        "minat_support",
    ]

    # 1. Kompetensi
    features_df["komp_jaringan"] = df[comp_map["jaringan_dasar"]].mean(axis=1)
    features_df["komp_admin"] = df[comp_map["administrasi_jaringan"]].mean(axis=1)
    features_df["komp_support"] = df[comp_map["technical_support"]].mean(axis=1)

    # 2. Minat
    features_df["minat_jaringan"] = df[int_map["minat_jaringan"]].mean(axis=1)
    features_df["minat_admin"] = df[int_map["minat_admin"]].mean(axis=1)
    features_df["minat_support"] = df[int_map["minat_support"]].mean(axis=1)

    # 3. Analisis Tambahan
    pplg_cols = [c for c in df.columns if c.startswith(config["mapping"]["pplg_prefix"])]
    if pplg_cols:
        features_df["skor_PPLG"] = df[pplg_cols].mean(axis=1)
    else:
        features_df["skor_PPLG"] = 0.0

    if "kehadiran" in df.columns:
        features_df["kehadiran"] = df["kehadiran"]
    else:
        features_df["kehadiran"] = 100.0

    for c in model_feature_cols:
        features_df[c] = pd.to_numeric(features_df[c], errors="coerce")

    X = features_df[model_feature_cols].copy()
    logger.info(f"Ekstraksi 6 fitur model berhasil untuk {len(features_df)} siswa.")
    return X, features_df
