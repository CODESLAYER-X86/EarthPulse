# Multi-Temporal NISAR Machine Learning Execution Report
**Project:** Dancing with SARs (NASA Space Apps Challenge 2026)  
**Study Area:** Potengi Estuary, Natal, RN, Brazil  
**Execution Timestamp:** 2026-11-10T17:49:15.191668Z  
**Model Architecture:** MiniBatchKMeans (k=4, Scaler=RobustScaler)

---

## 1. Executive Summary & Data Contract
- **Input Stack:** 12 multi-temporal NISAR L2 GCOV Frequency A bands (Cycles 028, 032, 033).
- **Spatial Resolution & Dimensions:** 10 m / 500 × 500 pixels (25 km²).
- **Coordinate Reference System:** EPSG:32725 (UTM Zone 25S).
- **Common-Valid Coverage:** 250000 / 250,000 pixels (100.00% valid observations).

---

## 2. Unsupervised Cluster Profiles & Radar Signatures

| Cluster | Interpretation | Pixel Count | Area (km²) | Area (%) | Mean HH_028 (dB) | Mean HV_028 (dB) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 0 | Low Backscatter / Smooth Surface (Estuarine Water & Intertidal Mudflats) | 50164 | 5.0164 | 20.07% | -12.57 dB | -20.01 dB |
| 1 | High Cross-Pol Backscatter / Volume Scattering (Dense Mangrove Forest Canopy) | 74700 | 7.47 | 29.88% | -6.13 dB | -12.26 dB |
| 2 | Intermediate Backscatter (Degraded Wetland, Scrub & Transitional Flats) | 55533 | 5.5533 | 22.21% | -10.94 dB | -21.12 dB |
| 3 | High Co-Pol Backscatter / Direct Scatterers (Urban Structures & Embankments) | 69603 | 6.9603 | 27.84% | -6.35 dB | -13.15 dB |

---

## 3. Scientific Integrity & Interpretation Notice
1. **Radar Signatures vs Ecological Ground-Truth:** Unsupervised clustering partitions the multi-dimensional radar backscatter state space. High cross-polarized HV backscatter with minimal temporal variation strongly corresponds to complex structural volume scattering (characteristic of mangrove canopies).
2. **Backscatter Dynamics:** Variations in HH and HV between August and October 2026 reflect physical changes in dielectric permittivity (soil/canopy moisture), tidal submersion, and surface roughness rather than deforestation or growth alone.
3. **Reproducibility:** This model uses fixed random seeds (seed=42) and standardized RobustScaler transformations, ensuring identical cluster convergence upon re-execution.
