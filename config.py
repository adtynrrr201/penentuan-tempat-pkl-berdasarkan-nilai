"""Config terpusat — satu-satunya tempat ubah parameter pipeline.

Ubah EPS/MIN_SAMPLES/FEATURE_COLS di sini, jangan di tengah logic.
"""
from pathlib import Path

# 10 variabel inti (6 nilai + 4 minat) — sesuai PRD §5.1
FEATURE_COLS = [
    "Programming_X",
    "Software_X",
    "SistemOperasi_XI",
    "Jaringan_XI",
    "Troubleshooting_XI",
    "Keamanan_XI",
    "Minat_Programming",
    "Minat_Networking",
    "Minat_Support",
    "Minat_Cybersecurity",
]

# Kelompok kolom per sumber file (join via ID_Siswa)
NILAI_COLS = [
    "Programming_X",
    "Software_X",
    "SistemOperasi_XI",
    "Jaringan_XI",
    "Troubleshooting_XI",
    "Keamanan_XI",
]
MINAT_COLS = [
    "Minat_Programming",
    "Minat_Networking",
    "Minat_Support",
    "Minat_Cybersecurity",
]
RAPORT_COLS = ["ID_Siswa", "Nama"] + NILAI_COLS + ["Kedisiplinan", "KerjaSama", "Penilaian_Guru"]
KUESIONER_COLS = ["ID_Siswa"] + MINAT_COLS

# DBSCAN — default 2.5 memberi 2-3 cluster pada dummy n=40 (StandardScaler 10D)
# Tuning: lihat k_distance_graph.png lalu ubah EPS; +0.5 → cluster lebih besar, -0.5 → lebih banyak noise
EPS = 2.5
MIN_SAMPLES = 5
K_DISTANCE_K = 2 * len(FEATURE_COLS)  # 20 — untuk k-distance graph (visual saja)
RANDOM_STATE = 42

# Paths
INPUT_RAPORT = "dataset_raport.xlsx"
INPUT_KUESIONER = "dataset_kuesioner.xlsx"
INPUT_DUDI = "dataset_dudi.xlsx"
OUTPUT_DIR = "output"

# Label kategori untuk profil cluster → Penilaian_Guru
KATEGORI_MAP = {
    "Programming_X": "Software",
    "Software_X": "Software",
    "Minat_Programming": "Software",
    "Jaringan_XI": "Network",
    "SistemOperasi_XI": "Network",
    "Minat_Networking": "Network",
    "Troubleshooting_XI": "Support",
    "Minat_Support": "Support",
    "Keamanan_XI": "Support",  # atau Cybersecurity jika berdiri sendiri
    "Minat_Cybersecurity": "Support",
}

# Validasi rentang
RENTANG_NILAI = (0, 100)  # untuk 6 kolom nilai
RENTANG_MINAT = (1, 5)
RENTANG_SIKAP = (1, 4)

# EKSPERIMEN — jangan aktifkan tanpa pairwise comparison matrix asli dari Waka Hubin + CR < 0.1
# DUDI_WEIGHTS = {"Networking": 0.25, "Support": 0.20, "Server_Cloud": 0.15, "Programming": 0.25, "Cybersecurity": 0.15}
# Default matching adalah Euclidean (tanpa bobot) — TOPSIS hanya opsional eksperimen (lihat prd.md Lampiran C)
DUDI_WEIGHTS = {
    "Networking": 0.20,
    "Support": 0.20,
    "Server_Cloud": 0.20,
    "Programming": 0.20,
    "Cybersecurity": 0.20,
}

# Output filenames
OUTPUT_FILES = {
    "hasil": Path(OUTPUT_DIR) / "hasil_klasterisasi.xlsx",
    "profil": Path(OUTPUT_DIR) / "profil_cluster.xlsx",
    "noise": Path(OUTPUT_DIR) / "laporan_noise.xlsx",
    "k_distance": Path(OUTPUT_DIR) / "k_distance_graph.png",
    "cluster_plot": Path(OUTPUT_DIR) / "hasil_cluster_plot.png",
}
