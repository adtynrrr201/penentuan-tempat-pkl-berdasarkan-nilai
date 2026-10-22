"""Modul generator data sintetis untuk pengujian pipeline skripsi.

DATA SINTETIS, BUKAN DATA SISWA.
"""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

from src.config import config


def generate_synthetic_data(n: int = 25, seed: int = 42) -> pd.DataFrame:
    """Menghasilkan DataFrame data sintetis siswa n=25 dengan 3 profil laten + outlier.

    DATA SINTETIS, BUKAN DATA SISWA.
    """
    np.random.seed(seed)
    
    codes = [f"SISWA_{i:03d}" for i in range(1, n + 1)]
    
    # 3 profil laten + 2-3 outlier
    # Profil 1: Jaringan Dasar (TJK tinggi)
    # Profil 2: Administrasi Jaringan (NA tinggi)
    # Profil 3: Technical Support (TS tinggi)
    
    profiles = np.random.choice([0, 1, 2], size=n, p=[0.33, 0.33, 0.34])
    
    tjk_i, tjk_ii = [], []
    na_i, na_iii = [], []
    ts_i, ts_ii = [], []
    
    pplg_1, pplg_2 = [], []
    attendance = []
    
    jar_1, jar_2, jar_3 = [], [], []
    adm_1, adm_2, adm_3 = [], [], []
    sup_1, sup_2, sup_3 = [], [], []
    
    for i, p in enumerate(profiles):
        if p == 0:
            # Jaringan Dasar tinggi
            tjk_i.append(np.random.normal(85, 5))
            tjk_ii.append(np.random.normal(88, 5))
            na_i.append(np.random.normal(65, 8))
            na_iii.append(np.random.normal(68, 8))
            ts_i.append(np.random.normal(70, 8))
            ts_ii.append(np.random.normal(72, 8))
            
            jar_1.append(np.random.choice([4, 5]))
            jar_2.append(np.random.choice([4, 5]))
            jar_3.append(np.random.choice([4, 5]))
            adm_1.append(np.random.choice([2, 3]))
            adm_2.append(np.random.choice([2, 3]))
            adm_3.append(np.random.choice([2, 3]))
            sup_1.append(np.random.choice([3, 4]))
            sup_2.append(np.random.choice([3, 4]))
            sup_3.append(np.random.choice([3, 4]))
        elif p == 1:
            # Administrasi Jaringan tinggi
            tjk_i.append(np.random.normal(70, 8))
            tjk_ii.append(np.random.normal(72, 8))
            na_i.append(np.random.normal(86, 5))
            na_iii.append(np.random.normal(89, 5))
            ts_i.append(np.random.normal(68, 8))
            ts_ii.append(np.random.normal(70, 8))
            
            jar_1.append(np.random.choice([2, 3]))
            jar_2.append(np.random.choice([2, 3]))
            jar_3.append(np.random.choice([2, 3]))
            adm_1.append(np.random.choice([4, 5]))
            adm_2.append(np.random.choice([4, 5]))
            adm_3.append(np.random.choice([4, 5]))
            sup_1.append(np.random.choice([3, 4]))
            sup_2.append(np.random.choice([3, 4]))
            sup_3.append(np.random.choice([3, 4]))
        else:
            # Technical Support tinggi
            tjk_i.append(np.random.normal(72, 8))
            tjk_ii.append(np.random.normal(74, 8))
            na_i.append(np.random.normal(70, 8))
            na_iii.append(np.random.normal(72, 8))
            ts_i.append(np.random.normal(87, 5))
            ts_ii.append(np.random.normal(90, 5))
            
            jar_1.append(np.random.choice([3, 4]))
            jar_2.append(np.random.choice([3, 4]))
            jar_3.append(np.random.choice([3, 4]))
            adm_1.append(np.random.choice([3, 4]))
            adm_2.append(np.random.choice([3, 4]))
            adm_3.append(np.random.choice([3, 4]))
            sup_1.append(np.random.choice([4, 5]))
            sup_2.append(np.random.choice([4, 5]))
            sup_3.append(np.random.choice([4, 5]))
            
        pplg_1.append(np.random.normal(75, 10))
        pplg_2.append(np.random.normal(78, 10))
        attendance.append(np.random.normal(95, 3))

    # Masukkan 2-3 outlier ekstrem
    for out_idx in [0, n // 2]:
        tjk_ii[out_idx] = 20.0
        na_iii[out_idx] = 22.0
        ts_ii[out_idx] = 19.0
        jar_1[out_idx] = 1
        jar_2[out_idx] = 1
        jar_3[out_idx] = 1

    data = {
        "kode_siswa": codes,
        "TJK_I": np.clip(tjk_i, 0, 100),
        "TJK_II": np.clip(tjk_ii, 0, 100),
        "NA_Muda_I": np.clip(na_i, 0, 100),
        "NA_Muda_III": np.clip(na_iii, 0, 100),
        "TS_I": np.clip(ts_i, 0, 100),
        "TS_II": np.clip(ts_ii, 0, 100),
        "PPLG_1": np.clip(pplg_1, 0, 100),
        "PPLG_2": np.clip(pplg_2, 0, 100),
        "kehadiran": np.clip(attendance, 50, 100),
        "JAR_1": np.clip(jar_1, 1, 5),
        "JAR_2": np.clip(jar_2, 1, 5),
        "JAR_3": np.clip(jar_3, 1, 5),
        "ADM_1": np.clip(adm_1, 1, 5),
        "ADM_2": np.clip(adm_2, 1, 5),
        "ADM_3": np.clip(adm_3, 1, 5),
        "SUP_1": np.clip(sup_1, 1, 5),
        "SUP_2": np.clip(sup_2, 1, 5),
        "SUP_3": np.clip(sup_3, 1, 5),
    }

    df = pd.DataFrame(data)
    return df


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic dataset for skripsi")
    parser.add_argument("--n", type=int, default=config["project"]["n_students"])
    parser.add_argument("--seed", type=int, default=config["project"]["seed"])
    parser.add_argument("--out", type=str, default=config["data_input"]["path"])
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_synthetic_data(n=args.n, seed=args.seed)
    df.to_excel(out_path, index=False)
    print(f"[INFO] DATA SINTETIS, BUKAN DATA SISWA. Tersimpan di {out_path} ({len(df)} baris).")


if __name__ == "__main__":
    main()
