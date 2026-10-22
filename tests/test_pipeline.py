"""Test suite untuk integrasi main.py."""
import subprocess
import sys
from pathlib import Path


def test_main_pipeline_execution():
    cmd = [sys.executable, "main.py"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Pipeline gagal: {res.stderr}"
    
    # Cek apakah file output tercipta
    assert Path("outputs/tables/hasil_pemetaan_lengkap.xlsx").exists()
    assert Path("outputs/hasil_ringkas.md").exists()
