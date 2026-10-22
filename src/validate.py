"""Modul validasi data: skema kolom, rentang nilai, duplikat, dan data kosong."""
import logging
from pathlib import Path
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)


def validate_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Melakukan validasi skema, rentang nilai (0-100 dan 1-5), duplikat ID, dan missing value.

    Menghasilkan laporan masalah tanpa mengubah data secara diam-diam.
    """
    report = {
        "total_rows_initial": len(df),
        "issues": [],
        "duplicates": 0,
        "missing_values": {},
        "out_of_range": {},
    }

    if df.empty:
        report["issues"].append("DataFrame kosong.")
        return df, report

    # 1. Cek Duplikat kode_siswa
    if "kode_siswa" in df.columns:
        dups = df.duplicated(subset=["kode_siswa"]).sum()
        report["duplicates"] = int(dups)
        if dups > 0:
            report["issues"].append(f"Ditemukan {dups} kode_siswa duplikat.")

    # 2. Cek Missing Values
    missing = df.isnull().sum().to_dict()
    report["missing_values"] = {k: int(v) for k, v in missing.items() if v > 0}
    if report["missing_values"]:
        report["issues"].append(f"Missing values terdeteksi: {report['missing_values']}")
        
        # Penanganan missing values sesuai config
        handling = config["data_input"].get("missing_handling", "mean")
        if handling == "drop":
            df = df.dropna()
            report["issues"].append("Missing values ditangani dengan menghapus baris.")
        elif handling in ["mean", "median"]:
            for col in df.select_dtypes(include=["number"]).columns:
                if df[col].isnull().any():
                    val = df[col].mean() if handling == "mean" else df[col].median()
                    df[col] = df[col].fillna(val)
            report["issues"].append(f"Missing values numerik diisi dengan {handling}.")

    # 3. Cek Rentang Nilai (0-100 untuk mapel/kehadiran, 1-5 untuk kuesioner)
    score_cols = []
    for field_list in config["mapping"]["competency"].values():
        score_cols.extend(field_list)
    score_cols.append("kehadiran")
    
    # Tambah PPLG cols jika ada
    pplg_cols = [c for c in df.columns if c.startswith(config["mapping"]["pplg_prefix"])]
    score_cols.extend(pplg_cols)

    for col in score_cols:
        if col in df.columns:
            invalid = ((df[col] < 0) | (df[col] > 100))
            n_inv = invalid.sum()
            if n_inv > 0:
                report["out_of_range"][col] = int(n_inv)
                report["issues"].append(f"Kolom {col} memiliki {n_inv} nilai di luar rentang 0-100.")

    likert_cols = []
    for field_list in config["mapping"]["interest"].values():
        likert_cols.extend(field_list)

    for col in likert_cols:
        if col in df.columns:
            invalid = ((df[col] < 1) | (df[col] > 5))
            n_inv = invalid.sum()
            if n_inv > 0:
                report["out_of_range"][col] = int(n_inv)
                report["issues"].append(f"Kolom {col} memiliki {n_inv} nilai Likert di luar rentang 1-5.")

    report["total_rows_final"] = len(df)
    logger.info(f"Validasi data selesai. Isu ditemukan: {len(report['issues'])}")
    return df, report


def validate_schema(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Alias untuk validate_data."""
    return validate_data(df)
