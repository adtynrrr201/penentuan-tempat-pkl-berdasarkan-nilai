"""End-to-end: generate dummy → main.ipynb pipeline → 5 outputs."""
import json
import sys
from pathlib import Path
import tempfile
import shutil


def test_full_pipeline(tmp_path=Path(tempfile.mkdtemp())):
    root = Path(__file__).resolve().parents[1]
    raport = tmp_path / "dataset_raport.xlsx"
    kuesioner = tmp_path / "dataset_kuesioner.xlsx"
    dudi = tmp_path / "dataset_dudi.xlsx"
    out = tmp_path / "output"

    import subprocess
    # generate
    r = subprocess.run([sys.executable, str(root / "generate_dummy_data.py"), "--n", "40", "--seed", "42", "--raport", str(raport), "--kuesioner", str(kuesioner), "--dudi", str(dudi), "--force"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert raport.exists() and kuesioner.exists() and dudi.exists()

    # execute main.ipynb code
    nb_path = root / "main.ipynb"
    assert nb_path.exists()
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    code_cells = [
        "".join(cell["source"])
        for cell in nb["cells"]
        if cell["cell_type"] == "code"
    ]
    full_code = "\n\n".join(code_cells)

    exec_globals = {
        "__file__": str(nb_path),
        "display": lambda *args, **kwargs: None,
    }
    exec(full_code, exec_globals)

    import pandas as pd
    out_file = Path("output") / "hasil_klasterisasi.xlsx"
    if not out_file.exists():
        out_file = tmp_path / "output" / "hasil_klasterisasi.xlsx"
    assert out_file.exists()
    df = pd.read_excel(out_file)
    assert "Cluster" in df.columns
