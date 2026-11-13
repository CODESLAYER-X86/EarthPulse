# Machine Learning Model & Radar Cluster Validation Report
**Project:** Dancing with SARs — NISAR L2 GCOV Temporal Analysis  
**Study Area:** Potengi Estuary, Natal, Brazil  
**Deliverable:** `data/reports/ml_validation_report.md`  
**Date:** 2026-11-11  

---

## 1. Model Objective & Architecture
The Machine Learning component is designed to solve an **unsupervised radiometric partitioning problem**:
> Group multi-temporal radar pixels exhibiting similar polarimetric signatures and temporal trajectories across the 60-day observation window without relying on unsubstantiated ground-truth labels.

- **Algorithm:** `MiniBatchKMeans` ($k=4$, batch size = 4,096, max iterations = 200, random state = 42).
- **Feature Scaling:** `RobustScaler` fitted across all 250,000 valid pixels on the 12 multi-temporal features (6 backscatter dB layers + 6 temporal difference layers).
- **Inertia:** 1,085,011.125.
- **Inference Mode:** Chunked spatial prediction preserving the original $500 \times 500$ grid, CRS `EPSG:32725`, and NoData convention.

---

## 2. Cluster Profiles & Radar Interpretation

| Cluster ID | Interpretation Hypothesis | Pixel Count | Area (km²) | Area (%) | Mean HH (dB) | Mean HV (dB) | Multi-Temporal Behavior |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | **Open Water & Smooth Mudflats** | 50,164 | 5.02 | 20.07% | -12.57 dB | -20.01 dB | Specular reflection, low backscatter across all dates. Slight tidal modulation (+1.2 dB). |
| **1** | **Dense Mangrove Canopy** | 74,700 | 7.47 | 29.88% | -6.13 dB | -12.26 dB | High cross-pol volume scattering with stable canopy persistence ($\Delta\text{HV} \approx -0.9\text{ dB}$). |
| **2** | **Transitional Scrub / Wetland** | 55,533 | 5.55 | 22.21% | -10.94 dB | -21.12 dB | Intermediate backscatter, high sensitivity to ground moisture and tidal borders. |
| **3** | **Urban & Structural Scatterers** | 69,603 | 6.96 | 27.84% | -6.35 dB | -13.15 dB | Strong co-polarized HH response (up to +31 dB) from buildings, bridges, and dry embankments. |

---

## 3. Methodological & Scientific Safeguards
1. **Absence of Ground Truth Claims:** Because continuous field-validated mangrove mortality/regrowth datasets were not available at the exact NISAR pass dates, this model explicitly avoids asserting supervised accuracy (e.g. fabricated confusion matrices or fake F1 scores).
2. **Separation from Physical Differences:** Unsupervised clusters are delivered as a distinct thematic layer (`ml_clusters`) that users can toggle independently of the empirical difference rasters (`diff_filtered`) and classified vector change zones.
3. **Provable Reproducibility:** Fixed random seeds, exact feature schemas, and serializable joblib artifacts ensure that model execution produces identical cluster centroids and spatial assignments across runs.
