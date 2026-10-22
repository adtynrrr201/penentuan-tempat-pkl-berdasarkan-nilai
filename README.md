# Skripsi DBSCAN — Klasterisasi PKL

Penerapan DBSCAN untuk klasterisasi profil kompetensi + minat siswa kelas XI TJKT sebagai dasar rekomendasi penempatan PKL berbasis kebutuhan DUDI.

## Prasyarat
- Python 3.10+ (tested 3.10–3.12)
- pip / uv

## Setup (sekali)
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cara Generate Data Dummy
Data asli belum ada? Pakai dummy 40 siswa (2 sumber, join via `ID_Siswa`):
```bash
python generate_dummy_data.py --n 40 --seed 42
# overwrite:
python generate_dummy_data.py --n 40 --seed 42 --force
# custom:
python generate_dummy_data.py --n 60 --seed 123 --raport dataset_raport.xlsx --kuesioner dataset_kuesioner.xlsx --dudi dataset_dudi.xlsx
```
Hasil:
- `dataset_raport.xlsx` (sheet Raport) — ID_Siswa, Nama, 6 nilai (0–100), Kedisiplinan, KerjaSama, Penilaian_Guru
- `dataset_kuesioner.xlsx` (sheet Kuesioner) — ID_Siswa + 4 minat (1–5)
- `dataset_dudi.xlsx` (sheet DUDI)

Hanya siswa yang ID-nya ada di **kedua** file yang dipakai (sisanya di-drop dengan warning).

## Cara Run (pipeline 12 langkah)
Buka dan jalankan Jupyter Notebook `main.ipynb`:
```bash
jupyter lab main.ipynb
# atau
jupyter notebook main.ipynb
```
Output di `output/`:
- `hasil_klasterisasi.xlsx` — siswa + Cluster + Kategori + Rekomendasi DUDI + Jarak_DUDI
- `profil_cluster.xlsx` — mean per cluster + Rekomendasi DUDI + Jarak_DUDI
- `laporan_noise.xlsx` — daftar noise (label -1)
- `k_distance_graph.png` — kurva k-distance + garis eps rekomendasi
- `hasil_cluster_plot.png` — scatter PCA per cluster

Log menampilkan silhouette, % kesesuaian guru, dan rekomendasi eps.

### Eksperimen Lanjutan (Opsional — Butuh Persetujuan Pembimbing)
Cell **Langkah 9** di `main.ipynb` sudah menjalankan Euclidean (resmi) + TOPSIS (eksperimen).
Jangan pakai hasil TOPSIS sebagai hasil resmi tanpa pairwise matrix + CR<0.1.
Output eksperimen tambah kolom `Skor_TOPSIS` + `Ranking_Top3` + `Gap_Terbesar`. Lihat `prd.md` Lampiran C.

## Cara Ubah Parameter
Edit `config.py` (satu-satunya sumber):
```python
EPS = 2.5
MIN_SAMPLES = 5
FEATURE_COLS = [...]  # 10 variabel inti
DUDI_WEIGHTS = {"Networking":0.25,"Support":0.20,"Server_Cloud":0.15,"Programming":0.25,"Cybersecurity":0.15} # AHP
```
Atau ubah langsung di cell **Langkah 4** (`eps`, `min_samples`) pada `main.ipynb`.

## Cara Test
```bash
pytest -q
pytest --cov=src --cov-report=term-missing  # coverage
pytest -k test_integration -xvs            # debug end-to-end
```

## Struktur Direktori
```
config.py  generate_dummy_data.py  main.ipynb  requirements.txt
src/  (data_loader, preprocessing, dbscan_runner, validation, profiling, matching, visualization, export)
tests/  output/
```

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `FileNotFoundError: dataset_raport.xlsx` | Jalankan `python generate_dummy_data.py --n 40` dulu |
| Semua jadi 1 cluster / semua noise | Tuning `EPS` di `config.py` (naikkan jika semua noise, turunkan jika 1 cluster); lihat `k_distance_graph.png` |
| `Penilaian_Guru` kosong → validasi kualitatif N/A | Normal — warning dicetak, pipeline tetap export |
| Silhouette `nan` | Terjadi jika <2 cluster (exclude noise); cek profil cluster |
| `ModuleNotFoundError: kneed` | `pip install kneed` atau fallback gradient sudah otomatis |
| `openpyxl` error | `pip install openpyxl` |

## Dokumen Terkait
- `prd.md` — PRD tunggal final (v1.1 TOPSIS terintegrasi)
