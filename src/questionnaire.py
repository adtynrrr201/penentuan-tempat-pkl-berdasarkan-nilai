"""Modul kuesioner: validitas butir (korelasi item-total terkoreksi) dan Cronbach's alpha."""
import logging
import numpy as np
import pandas as pd

from src.config import config

logger = logging.getLogger(__name__)


def compute_cronbach_alpha(items_df: pd.DataFrame) -> float:
    """Menghitung Cronbach's alpha menggunakan numpy murni."""
    items = items_df.values
    n_items = items.shape[1]
    if n_items < 2:
        return 0.0
    item_variances = np.var(items, axis=0, ddof=1)
    total_score = np.sum(items, axis=1)
    total_variance = np.var(total_score, ddof=1)
    if total_variance == 0:
        return 0.0
    alpha = (n_items / (n_items - 1)) * (1 - (np.sum(item_variances) / total_variance))
    return float(alpha)


def analyze_questionnaire(df: pd.DataFrame) -> dict:
    """Menganalisis validitas butir dan reliabilitas (Cronbach's alpha) per bidang.

    Menampilkan pembanding r tabel 5% untuk n=25, df=23 (0,396).
    JANGAN membuang butir otomatis.
    """
    results = {}
    r_table_threshold = config["dbscan"]["r_table_threshold"]

    for bidang, items in config["mapping"]["interest"].items():
        valid_items = [item for item in items if item in df.columns]
        if not valid_items:
            continue
        sub_df = df[valid_items]
        
        # Cronbach alpha
        alpha = compute_cronbach_alpha(sub_df)
        
        # Item-total corrected correlation
        item_stats = {}
        total_score = sub_df.sum(axis=1)
        
        for item in valid_items:
            item_vals = sub_df[item]
            # corrected total: total score minus current item
            corrected_total = total_score - item_vals
            if np.std(item_vals) == 0 or np.std(corrected_total) == 0:
                corr = 0.0
            else:
                corr = np.corrcoef(item_vals, corrected_total)[0, 1]
            
            item_stats[item] = {
                "r_corrected": float(corr),
                "valid": bool(corr >= r_table_threshold),
            }
            
        results[bidang] = {
            "cronbach_alpha": alpha,
            "item_stats": item_stats,
            "threshold": r_table_threshold,
        }

    logger.info("Analisis kuesioner (validitas & reliabilitas) selesai.")
    return results
