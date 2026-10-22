import pandas as pd
import tempfile
from pathlib import Path

from generate_dummy_data import generate_siswa, generate_dudi, split_siswa
from src.data_loader import load_data, validate_input
import config


def test_validate_drops_out_of_range():
    df = generate_siswa(n=10, seed=1)
    df.loc[0, "Programming_X"] = 999
    df.loc[1, "Minat_Programming"] = 99
    df_clean, warns = validate_input(df, is_siswa=True)
    assert len(df_clean) < len(df)
    assert any("di luar" in w for w in warns)


def test_validate_missing_becomes_nan_then_drop():
    df = generate_siswa(n=10, seed=2)
    df.loc[0, "Jaringan_XI"] = "bukan angka"
    # coerce akan jadi NaN lalu di-drop
    df["Jaringan_XI"] = pd.to_numeric(df["Jaringan_XI"], errors="coerce")
    df_clean, _ = validate_input(df, is_siswa=True)
    assert len(df_clean) == 9


def test_load_data_roundtrip(tmp_path: Path = Path(tempfile.mkdtemp())):
    r = tmp_path / "r.xlsx"
    k = tmp_path / "k.xlsx"
    d = tmp_path / "d.xlsx"
    df_raport, df_kuesioner = split_siswa(generate_siswa(n=15, seed=3))
    df_raport.to_excel(r, index=False)
    df_kuesioner.to_excel(k, index=False)
    generate_dudi().to_excel(d, index=False)
    df_s, df_d, warns = load_data(r, k, d)
    assert len(df_s) == 15
    assert len(df_d) >= 5


def test_load_data_merge_drops_mismatched_ids(tmp_path: Path = Path(tempfile.mkdtemp())):
    r = tmp_path / "r.xlsx"
    k = tmp_path / "k.xlsx"
    d = tmp_path / "d.xlsx"
    df_raport, df_kuesioner = split_siswa(generate_siswa(n=10, seed=4))
    # 1 ID hanya ada di raport, 1 ID hanya ada di kuesioner
    df_kuesioner = df_kuesioner.iloc[1:].copy()
    extra = df_kuesioner.iloc[[0]].copy()
    extra["ID_Siswa"] = "S999"
    df_kuesioner = pd.concat([df_kuesioner, extra], ignore_index=True)
    df_raport.to_excel(r, index=False)
    df_kuesioner.to_excel(k, index=False)
    generate_dudi().to_excel(d, index=False)
    df_s, _, warns = load_data(r, k, d)
    assert len(df_s) == 9
    assert "S999" not in set(df_s["ID_Siswa"].astype(str))
    assert any("hanya ada di" in w for w in warns)
