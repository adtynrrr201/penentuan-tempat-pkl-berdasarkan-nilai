"""load_data & validate_input — load Excel, cek missing/tipe/rentang."""
import warnings
from pathlib import Path

import pandas as pd

import config

SISWA_REQUIRED = ["ID_Siswa"] + config.FEATURE_COLS
DUDI_REQUIRED = ["Nama_DUDI", "Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]
SIKAP_COLS = ["Kedisiplinan", "KerjaSama"]
DUDI_COLS = ["Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]


def _drop_out_of_range(df: pd.DataFrame, checks: list[tuple[str, float, float]], label: str) -> tuple[pd.DataFrame, list[str]]:
    """Drop baris dengan nilai di luar rentang / NaN pada kolom numerik. Return (df_clean, warnings)."""
    warns: list[str] = []
    if df.empty:
        return df, warns
    mask_invalid = pd.Series(False, index=df.index)
    for col, lo, hi in checks:
        if col not in df.columns:
            warns.append(f"{label}: kolom {col} tidak ditemukan")
            continue
        bad = ((df[col] < lo) | (df[col] > hi) | df[col].isna())
        if bad.any():
            warns.append(f"{label} {col}: {bad.sum()} nilai di luar {lo}–{hi}/NaN → baris di-drop")
        mask_invalid |= bad
    before = len(df)
    if mask_invalid.any():
        df = df[~mask_invalid].copy()
        warns.append(f"{label}: drop {mask_invalid.sum()} baris invalid (dari {before} → {len(df)})")
    return df, warns


def _drop_duplicate_ids(df: pd.DataFrame, label: str) -> tuple[pd.DataFrame, list[str]]:
    """Drop duplikat ID_Siswa (keep first). Return (df_clean, warnings)."""
    warns: list[str] = []
    if df.empty or "ID_Siswa" not in df.columns:
        return df, warns
    dup = df.duplicated(subset="ID_Siswa", keep="first")
    if dup.any():
        ids = sorted(df.loc[dup, "ID_Siswa"].astype(str).unique().tolist())
        warns.append(f"{label}: {dup.sum()} duplikat ID_Siswa {ids[:5]} → keep first")
        df = df[~dup].copy()
    return df, warns


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, list[str]]:
    warns = []
    for c in cols:
        if c not in df.columns:
            warns.append(f"Kolom {c} tidak ditemukan")
            continue
        df[c] = pd.to_numeric(df[c], errors="coerce")
        n_nan = df[c].isna().sum()
        if n_nan > 0:
            warns.append(f"{c}: {n_nan} nilai non-numerik → NaN")
    return df, warns


def validate_input(df: pd.DataFrame, is_siswa: bool = True) -> tuple[pd.DataFrame, list[str]]:
    """Validasi rentang & drop baris invalid. Return (df_clean, warnings)."""
    warns: list[str] = []
    if df.empty:
        warns.append("DataFrame kosong")
        return df, warns

    # cek kolom wajib
    required = SISWA_REQUIRED if is_siswa else DUDI_REQUIRED
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        warns.append(f"Kolom wajib hilang: {missing_cols}")

    if is_siswa:
        # rentang nilai 0-100
        nilai_cols = ["Programming_X", "Software_X", "SistemOperasi_XI", "Jaringan_XI", "Troubleshooting_XI", "Keamanan_XI"]
        minat_cols = ["Minat_Programming", "Minat_Networking", "Minat_Support", "Minat_Cybersecurity"]
        for c in nilai_cols:
            if c in df.columns:
                out = ((df[c] < 0) | (df[c] > 100)) & df[c].notna()
                if out.any():
                    warns.append(f"{c}: {out.sum()} nilai di luar 0–100 → baris di-drop")
        for c in minat_cols:
            if c in df.columns:
                out = ((df[c] < 1) | (df[c] > 5)) & df[c].notna()
                if out.any():
                    warns.append(f"{c}: {out.sum()} nilai di luar 1–5 → baris di-drop")

        # drop baris dengan FEATURE_COLS NaN atau out-of-range
        before = len(df)
        # coerce sudah dilakukan caller
        mask_invalid = pd.Series(False, index=df.index)
        for c in config.FEATURE_COLS:
            if c in df.columns:
                if c in nilai_cols:
                    mask_invalid |= (df[c] < 0) | (df[c] > 100) | df[c].isna()
                else:
                    mask_invalid |= (df[c] < 1) | (df[c] > 5) | df[c].isna()
        if mask_invalid.any():
            df = df[~mask_invalid].copy()
            warns.append(f"Drop {mask_invalid.sum()} baris invalid (dari {before} → {len(df)})")
    else:
        dudi_cols = ["Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]
        for c in dudi_cols:
            if c in df.columns:
                out = ((df[c] < 1) | (df[c] > 5)) & df[c].notna()
                if out.any():
                    warns.append(f"DUDI {c}: {out.sum()} di luar 1–5")

    return df, warns


def load_data(raport_path: str | Path = "data/raw/data_dummy_tjkt_25_siswa.xlsx",
            kuesioner_path: str | Path = "data/raw/data_dummy_tjkt_25_siswa.xlsx"):
    raport_path = Path(raport_path)
    if not raport_path.exists():
        raise FileNotFoundError(f"File raport tidak ditemukan: {raport_path}")
    df = pd.read_excel(raport_path, sheet_name=0, engine="openpyxl")
    return df, df
    warns.extend(w7)

    # merge via ID_Siswa (inner) — ID yang hanya ada di satu sisi di-drop
    if "ID_Siswa" not in df_r.columns or "ID_Siswa" not in df_k.columns:
        warns.append("Kolom ID_Siswa hilang di raport/kuesioner — hasil merge kosong")
        df_siswa = pd.DataFrame()
    else:
        ids_r = set(df_r["ID_Siswa"].astype(str))
        ids_k = set(df_k["ID_Siswa"].astype(str))
        only_r = sorted(ids_r - ids_k)
        only_k = sorted(ids_k - ids_r)
        if only_r:
            warns.append(f"Merge: {len(only_r)} ID hanya ada di raport (contoh: {only_r[:5]}) → di-drop")
        if only_k:
            warns.append(f"Merge: {len(only_k)} ID hanya ada di kuesioner (contoh: {only_k[:5]}) → di-drop")
        df_siswa = df_r.merge(df_k, on="ID_Siswa", how="inner")
        # urutan kolom stabil: ID, Nama, 6 nilai, 4 minat, sikap, guru + ekstra
        base = (["ID_Siswa", "Nama"] + config.NILAI_COLS + config.MINAT_COLS
                + SIKAP_COLS + ["Penilaian_Guru"])
        ordered = [c for c in base if c in df_siswa.columns]
        extra = [c for c in df_siswa.columns if c not in ordered]
        df_siswa = df_siswa[ordered + extra].copy()

    # validasi akhir df gabungan (FEATURE_COLS) + DUDI
    df_siswa, w8 = validate_input(df_siswa, is_siswa=True)
    df_dudi, w9 = validate_input(df_dudi, is_siswa=False)
    warns.extend(w8)
    warns.extend(w9)

    return df_siswa, df_dudi, warns
