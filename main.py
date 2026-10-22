#!/usr/bin/env python
# coding: utf-8

# # Pipeline Pemetaan Kecenderungan Bidang PKL Siswa Kelas XI TJKT
# Notebook interaktif ini berisi 12 langkah alur kerja lengkap (Load, Validasi, Kuesioner, Preprocessing, Klasterisasi K-Means, Hierarchical Ward, DBSCAN, Stabilitas, Validasi, Profiling, PPLG, dan Export).

# ## 1. Load Data & Validasi Schema

# In[3]:


import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import config
from src.data_loader import load_data
from src.validate import validate_data

df_siswa, df_kuesioner = load_data()
df_valid, problem_report = validate_data(df_siswa)
print(f"Jumlah baris valid: {len(df_valid)}")
print(problem_report)


# ## 2. Analisis Kuesioner (Cronbach Alpha & Item-Total Correlation)

# In[ ]:


from src.questionnaire import analyze_questionnaire
reliability_df = analyze_questionnaire(df_valid)
print(reliability_df)


# ## 3. Ekstraksi Fitur & Preprocessing (IQR Outlier & StandardScaler)

# In[ ]:


from src.features import extract_features
from src.preprocess import preprocess, scale_features

X_raw, df_features = extract_features(df_valid)
X_clean, outliers = preprocess(df_features)
X_scaled, scaler = scale_features(X_clean)
print(f"Dimensi data scaled: {X_scaled.shape}")
print(f"Jumlah outlier terdeteksi via IQR: {len(outliers)}")


# ## 4. K-Means Clustering (k=2..4)

# In[ ]:


from src.kmeans_model import run_kmeans_pipeline
kmeans_results = run_kmeans_pipeline(X_scaled)
best_k = max(kmeans_results, key=lambda k: kmeans_results[k]["silhouette"])
best_kmeans_labels = kmeans_results[best_k]["labels"]
print(f"K-Means terbaik (k={best_k})")


# ## 5. Hierarchical Clustering (Ward Linkage)

# In[ ]:


from src.hierarchical_model import run_hierarchical_pipeline
hier_result = run_hierarchical_pipeline(X_scaled, k_target=best_k)
hier_labels = hier_result["labels"]
cophenetic_c = hier_result["cophenetic_correlation"]
print(f"Hierarchical Ward selesai. Cophenetic c = {cophenetic_c:.4f}")


# ## 6. DBSCAN Clustering & k-Distance Graph

# In[ ]:


from src.dbscan_runner import run_dbscan, k_distance_graph
k_distance_graph(X_scaled)
dbscan_labels = run_dbscan(X_scaled)
n_noise = sum(dbscan_labels == -1)
print(f"Jumlah noise DBSCAN: {n_noise}")


# ## 7. Evaluasi Kestabilan & Kesepakatan Klaster

# In[ ]:


from src.stability import evaluate_kmeans_stability, evaluate_subsample_stability
from src.agreement import compute_agreement

km_stab = evaluate_kmeans_stability(X_scaled, best_kmeans_labels)
sub_stab = evaluate_subsample_stability(X_scaled, best_k)
agreement = compute_agreement(best_kmeans_labels, hier_labels)

print("Stabilitas K-Means (100 seed):", km_stab)
print("Stabilitas Subsample (80%):", sub_stab)
print("Kesepakatan K-Means vs Hierarchical (ARI):", agreement["ARI"])


# ## 8. Profiling Cluster & Pemetaan Kecenderungan Bidang

# In[ ]:


from src.profiling import profile_and_label_clusters
profile_df, df_mapped = profile_and_label_clusters(df_features, best_kmeans_labels)
print(profile_df)
print(df_mapped[["kode_siswa", "kode_siswa", "cluster", "kecenderungan_bidang"]].head(10))


# ## 9. Analisis Tambahan Nilai PPLG Kelas 10

# In[ ]:


from src.pplg_analysis import analyze_pplg_scores
pplg_stats = analyze_pplg_scores(df_mapped, best_kmeans_labels)
print(pplg_stats)


# ## 10. Pembuatan Template Penilai (Rater Validation)

# In[ ]:


from src.rater_validation import generate_rater_template
template_path = generate_rater_template(df_mapped, "outputs/tables/template_penilai.csv")
print(f"Template penilai berhasil dibuat di: {template_path}")


# ## 11. Export Hasil Lengkap ke Excel

# In[ ]:


from src.report import export_pipeline_results
export_paths = export_pipeline_results(df_mapped, profile_df, pplg_stats)
print("Export berhasil:", export_paths)


# In[ ]:


# ## 13. Visualisasi Grafik Interaktif untuk Penilaian Penempatan PKL
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Plot Distribusi Kecenderungan Bidang
sns.countplot(data=df_mapped, x="kecenderungan_bidang", ax=axes[0], palette="viridis")
axes[0].set_title("Distribusi Kecenderungan Bidang PKL")
axes[0].set_xlabel("Kecenderungan Bidang")
axes[0].set_ylabel("Jumlah Siswa")
axes[0].tick_params(axis='x', rotation=15)

# 2. Plot Perbandingan Komponen per Cluster
cluster_melt = df_mapped.melt(id_vars=["kode_siswa", "cluster"], 
                              value_vars=["komp_jaringan", "komp_admin", "komp_support"],
                              var_name="Kompetensi", value_name="Nilai")
sns.boxplot(data=cluster_melt, x="Kompetensi", y="Nilai", hue="cluster", ax=axes[1], palette="Set2")
axes[1].set_title("Distribusi Nilai Kompetensi berdasarkan Cluster")
axes[1].set_xlabel("Jenis Kompetensi")
axes[1].set_ylabel("Nilai Rata-rata")

plt.tight_layout()
plt.savefig("outputs/figures/grafik_analisis_penilaian.png", dpi=300)
plt.show()

