# MASTER PLAN — Dancing with SARs
## Multi-Temporal NISAR L2 GCOV Surface Change & Estuarine Monitoring

### 1. Executive Summary
- **Mission:** NASA Space Apps Challenge 2026
- **Objective:** Detect surface and wetland dynamics in the Potengi Estuary (Natal, RN, Brazil) across three repeat NISAR L2 GCOV acquisitions (August – October 2026).
- **Core Strategy:** Multi-agent division of labor combining rigorous radar processing (OpenCode), machine learning clustering & change analysis (Claude), and an interactive web visualization platform (Antigravity).

---

### 2. Architecture & Data Flow

```
NASA NISAR L2 GCOV (Cycles 028, 032, 033)
                │
                ▼
       [OpenCode Data Engine]
  Windowed extraction (500x500, EPSG:32725)
  dB conversion & common-valid masking
  Temporal differencing & 12-band stack
                │
                ├──► data/processed/ (HH/HV linear & dB rasters)
                ├──► data/temporal/ (6 difference rasters + mask)
                └──► data/ml/feature_stack.tif + feature_metadata.json
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
      [Claude ML Engine]              [Antigravity Web App]
   MiniBatch K-Means (k=4)            FastAPI backend + REST API
   Statistical change categories      React + MapLibre GL frontend
   Model & scaler artifacts           Temporal swipe & layer toggle
   Cluster centroids & statistics     Recharts scientific dashboards
               │                                 ▲
               └─────────────────────────────────┘
```

---

### 3. Key Technical Decisions
- **AOI:** Potengi Estuary (UTM 25S, EPSG:32725, 25 km², 10m spacing).
- **Acquisitions:**
  - Cycle 028: 2026-08-22
  - Cycle 032: 2026-10-09
  - Cycle 033: 2026-10-21
- **Polarizations:** HH and HV (Frequency A).
- **Mask Convention:** `(mask >= 1) & (mask <= 254) & isfinite(HH) & (HH > 0) & isfinite(HV) & (HV > 0)`.
- **Temporal Diffs:** 6 pairwise differences (3 HH, 3 HV).
- **ML Algorithm:** MiniBatch K-Means (unsupervised clustering of radar response patterns) + Statistical Change Detection.
- **Scientific Integrity Rule:** Radar backscatter changes are observations, not verified ground truth mangrove loss/gain without in-situ labels.
