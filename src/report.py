"""Modul pelaporan: export workbook Excel dengan sheet terpisah, ringkasan Markdown, dan logging."""
import logging
from pathlib import Path
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)


def export_pipeline_results(df_clustered: pd.DataFrame, profile_df: pd.DataFrame, pplg_stats: pd.DataFrame) -> dict:
    """Mengekspor seluruh hasil ke satu workbook Excel terpisah dan membuat hasil_ringkas.md."""
    output_dir = Path(config["paths"]["output_dir"])
    tables_dir = Path(config["paths"]["tables_dir"])
    tables_dir.mkdir(parents=True, exist_ok=True)

    excel_path = tables_dir / "hasil_pemetaan_lengkap.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_clustered.to_excel(writer, sheet_name="Siswa_Cluster", index=False)
        profile_df.to_excel(writer, sheet_name="Profil_Cluster")
        pplg_stats.to_excel(writer, sheet_name="Analisis_PPLG", index=False)

    # Ringkasan Markdown
    summary_path = output_dir / "hasil_ringkas.md"
    summary_content = f"""# Ringkasan Hasil Penelitian Skripsi
- **Judul**: {config['project']['title']}
- **Catatan**: {config['project']['author_note']}
- **Jumlah Siswa**: {len(df_clustered)}
- **File Excel Utama**: `{excel_path}`

## Daftar Keterbatasan Metodologis
1. Sampel sangat kecil ($n=25$ siswa); semua hasil adalah studi kasus dan tidak dapat digeneralisasi.
2. Tidak ada uji signifikansi pada perbandingan cluster sesuai sifat eksploratif tanpa asumsi distribusi normal.
3. DBSCAN sangat sensitif terhadap pemilihan parameter `eps` dan `min_samples`.
"""
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_content)

    logger.info(f"Export selesai. Excel: {excel_path}, Ringkasan: {summary_path}")
    return {"excel": str(excel_path), "summary": str(summary_path)}
