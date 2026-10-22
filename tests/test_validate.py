"""Test suite untuk modul validate.py."""
import pandas as pd
import pytest
from src.validate import validate_data


def test_validate_data_clean():
    df = pd.DataFrame({
        "kode_siswa": ["S001", "S002"],
        "TJK_I": [80, 85],
        "TJK_II": [82, 88],
        "JAR_1": [4, 5],
    })
    df_clean, report = validate_data(df)
    assert len(df_clean) == 2
    assert report["total_rows_initial"] == 2
    assert len(report["issues"]) == 0


def test_validate_data_out_of_range():
    df = pd.DataFrame({
        "kode_siswa": ["S001"],
        "TJK_I": [120],  # Invalid (> 100)
        "JAR_1": [6],    # Invalid (> 5)
    })
    df_clean, report = validate_data(df)
    assert len(report["out_of_range"]) == 2
