# Dancing with SARs
### Multi-Temporal NISAR L2 GCOV Surface Change & Estuarine Monitoring
**NASA Space Apps Challenge 2026**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)
[![MapLibre GL](https://img.shields.io/badge/MapLibre_GL-5.1+-3bb2d0.svg)](https://maplibre.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Project Overview
**Dancing with SARs** is an interactive, scientific Earth observation and machine-learning platform designed to monitor multi-temporal radar surface changes across the **Potengi Estuary** (Natal, Rio Grande do Norte, Brazil) using repeat-pass **NASA-ISRO Synthetic Aperture Radar (NISAR)** L2 GCOV observations.

### Key Objectives
- **Temporal Radar Tracking:** Analyze dual-polarization (HH & HV) gamma-zero backscatter power over three NISAR acquisitions spanning 60 days in 2026.
- **Statistical Change Detection:** Delineate measurable backscatter increase, stability, and decrease across repeat observations.
- **Unsupervised ML Radar Clustering:** Group multi-temporal radar response profiles with `MiniBatchKMeans` to reveal structural vegetation (mangrove canopy), tidal water/mudflat dynamics, and urban scatterers.
- **Interactive Visualization:** Provide an intuitive MapLibre GL geospatial map, layer switcher, temporal progression charts, and verified scientific provenance reports.

---

## 2. Satellite Data & Study Area
- **Sensor:** NASA-ISRO Synthetic Aperture Radar (NISAR)
- **Product:** Level-2 Geocoded Polarimetric Covariance (GCOV), Frequency A (L-band)
- **Study Area:** Potengi Estuary, Natal, RN, Brazil
- **Coordinate Reference System:** `EPSG:32725` (UTM Zone 25S)
- **Dimensions & Resolution:** 500 × 500 pixels (10.0 m spacing, 25.0 km² area)
- **Acquisitions:**
  - **Cycle 028:** 2026-08-22 (August Baseline)
  - **Cycle 032:** 2026-10-09 (48 days post-baseline)
  - **Cycle 033:** 2026-10-21 (Exact 12-day repeat orbit)
- **Coverage Quality:** 100.00% common-valid radar samples across all three dates.

---

## 3. System Architecture & Tech Stack

```
NASA NISAR L2 GCOV (Cycles 028, 032, 033)
                │
                ▼
       [Data Engineering Engine]
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
         [ML Engine]                     [Web Platform]
   MiniBatch K-Means (k=4)            FastAPI backend + REST API
   Statistical change categories      React + MapLibre GL frontend
   Model & scaler artifacts           Temporal swipe & layer toggle
   Cluster centroids & statistics     Recharts scientific dashboards
```

- **Backend:** Python 3.12, FastAPI, Uvicorn, Rasterio, NumPy, Matplotlib
- **Machine Learning:** Scikit-learn (`MiniBatchKMeans`, `RobustScaler`), Joblib
- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, MapLibre GL, Recharts, Lucide Icons

---

## 4. Quickstart & Local Execution

### Prerequisites
- Python 3.12+ with virtual environment
- Node.js 20+ & npm (for editing the frontend)

### Launch the Application
To run the full integrated system (FastAPI backend serving the built React SPA):

```bash
# 1. Run the launcher
./.venv/bin/python run_app.py
```
Open your browser at: **`http://localhost:8000`**

### Running the End-to-End Tests
To verify all APIs, dynamic raster rendering, and ML endpoints:

```bash
./.venv/bin/python tests/test_integration.py
```

### Reproducing the ML Pipeline
To retrain and regenerate predictions and reports:

```bash
./.venv/bin/python ml_engine/run_ml.py run-all
```

---

## 5. Scientific Interpretation & Transparency Notice
1. **Radar Observations vs Ecological Truth:** Radar backscatter variations represent physical interactions with surface geometry, dielectric constant, and roughness (e.g. tidal inundation, soil moisture, canopy structure). They are not labeled ground-truth deforestation or growth events without in-situ validation.
2. **Cluster Profiles:** The unsupervised $k=4$ clustering groups multi-temporal radar behaviors:
   - **Cluster 0 (20.07%):** Low backscatter (Water & intertidal mudflats)
   - **Cluster 1 (29.88%):** High cross-pol HV backscatter (Dense mangrove forest canopy)
   - **Cluster 2 (22.21%):** Intermediate backscatter (Transitional scrub & degraded wetland)
   - **Cluster 3 (27.84%):** High co-pol HH backscatter (Urban structures & embankments)
