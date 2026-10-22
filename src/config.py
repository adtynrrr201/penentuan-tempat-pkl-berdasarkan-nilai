"""Modul konfigurasi terpusat memuat config.yaml."""
from pathlib import Path
import yaml

CONFIG_PATH = Path("config.yaml")


def load_config(path: Path | str = CONFIG_PATH) -> dict:
    """Memuat file konfigurasi YAML."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File konfigurasi tidak ditemukan: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = load_config()
