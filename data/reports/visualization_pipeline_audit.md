# Technical Audit: SAR Visualization & Processing Pipeline
**Project:** Dancing with SARs — NISAR L2 GCOV Temporal Analysis  
**Study Area:** Potengi Estuary, Natal, Rio Grande do Norte, Brazil  
**Document:** `data/reports/visualization_pipeline_audit.md`  
**Date:** 2026-11-11  

---

## 1. Executive Summary

This audit investigates the scientific and perceptual failure modes in the current SAR visualization pipeline. In the initial prototype, users are presented with a dense 500×500 grid of raw red-and-blue pixels superimposed over the map. This presentation obscures the underlying estuarine geography, confuses random speckle fluctuations with genuine surface change, and fails to communicate actionable environmental insights.

The purpose of this audit is to identify the root mathematical and architectural causes of this issue and define the corrective implementation roadmap across Phases 2 through 9.

---

## 2. Architecture & Technology Stack Audit

| Component | Current Implementation | Technical Status |
| :--- | :--- | :--- |
| **Frontend Framework** | React 19 + TypeScript + Vite | Healthy, fast compilation |
| **Mapping Engine** | MapLibre GL 5.1.1 | Functional, supports `ImageSource` and GeoJSON layers |
| **Backend Framework** | Python 3.12 + FastAPI + Uvicorn | High performance, local execution |
| **Geospatial Processing** | Rasterio 1.5.2, NumPy 2.5.4, PyProj | Compliant with EPSG:32725 and EPSG:4326 |
| **Visualization / Charting** | Recharts 2.15.1 | Functional, needs richer scientific metadata |
| **Storage Formats** | Single/Multi-band Cloud-Optimized GeoTIFF | Standardized in `data/processed/`, `data/temporal/` |
| **ML Engine** | Scikit-learn (`MiniBatchKMeans`, `RobustScaler`) | Functional in `ml_engine/run_ml.py` |

---

## 3. NISAR L2 GCOV Observation Verification

All three acquisitions were inspected directly from the original HDF5 granules:

1. **Cycle 028:** 
   - Zero Doppler Start: `2026-08-22T20:37:40.000` (Orbit 5601, Track 139, Descending)
   - Polarizations: HH, HV (Frequency A, 10 m pixel spacing)
2. **Cycle 032:** 
   - Zero Doppler Start: `2026-10-09T20:37:40.000` (Orbit 6293, Track 139, Descending)
   - 48 days post-baseline; identical track geometry and grid.
3. **Cycle 033:** 
   - Zero Doppler Start: `2026-10-21T20:37:40.000` (Orbit 6466, Track 139, Descending)
   - Exact 12-day repeat orbit after Cycle 032 (60 days from baseline).

**Spatial Alignment Verification:**
- Common CRS: `EPSG:32725` (UTM Zone 25S).
- Raster Dimensions: 500 rows × 500 columns (25.0 km²).
- Affine Transform: `[10.0, 0.0, 251880.0, 0.0, -10.0, 9365260.0, 0.0, 0.0, 1.0]`.
- Geographic Center: $35.218^\circ\text{W}, 5.761^\circ\text{S}$ (Potengi Estuary).
- Common-Valid Coverage: 250,000 / 250,000 pixels (100.00% valid radar coverage).

---

## 4. Root Cause Diagnosis of Visualization Problems

### Diagnostic Test 1: Units and Conversions
- **Observation:** Linear power $\gamma^0_{\text{linear}}$ was converted to decibels ($\gamma^0_{\text{dB}} = 10 \log_{10}(\gamma^0_{\text{linear}})$).
- **Issue:** Difference was computed as a direct point subtraction $\Delta \text{dB} = \text{dB}_{\text{target}} - \text{dB}_{\text{baseline}}$ on unfiltered pixels. While mathematically equal to $10 \log_{10}(P_{\text{target}} / P_{\text{baseline}})$, applying it to un-speckled data exaggerates noise.

### Diagnostic Test 2: Low Equivalent Number of Looks (ENL) and Severe Speckle
- **Measurements on Homogeneous Targets:**
  - Water Homogeneous ROI: $\text{ENL} \approx 1.60$ (HH), $1.46$ (HV)
  - Mangrove Canopy ROI: $\text{ENL} \approx 2.04$ (HH), $1.74$ (HV)
- **Impact:** An ENL of $\sim 1.7$ means single-pixel radar backscatter suffers from high multiplicative speckle variance ($\sigma_{\text{speckle}} \approx \pm 2.86\text{ dB}$).
- Over $72\%$ of all pixels fluctuate within $\pm 3.0\text{ dB}$ purely due to Rayleigh/Gaussian fading statistics.
- By stretching raw differences from $-6\text{ dB}$ to $+6\text{ dB}$ with a continuous red-to-blue colormap, the display treats pure radar noise as massive environmental change.

### Diagnostic Test 3: Full-AOI Opaque Coverage
- The entire 25 km² rectangular bounding box is rendered as an opaque raster, covering city streets, river channels, and coastal dunes identically without morphological isolation or spatial filtering.
- Users cannot tell where the estuarine wetland actually is versus urban dry land.

### Diagnostic Test 4: Lack of Coherent Change Region Extraction
- There was no spatial grouping, connected-component analysis, or minimum mapping unit (MMU) filter. Real environmental phenomena (like tidal mudflat inundation or mangrove canopy defoliation) occur across contiguous spatial clusters, whereas noise occurs at the single-pixel scale.

---

## 5. Corrective Action Plan

To transition from an opaque pixel-noise viewer to a scientifically rigorous environmental platform, the following corrections will be implemented:

1. **Phase 2 — SAR Processing Pipeline Correction:**
   - Implement an **Adaptive Enhanced Lee Filter** operating in the linear power domain ($5\times 5$ window, damping factor $=1$, local variance weighting) to suppress speckle while preserving sharp edges (e.g., riverbanks, mangrove boundaries).
   - Recompute all backscatter dB layers and pairwise temporal differences on the filtered products.
   - Retain both raw and filtered layers so users can toggle between raw sensor measurements and filtered products.
2. **Phase 3 — Environmental Change Classification & Vector Region Extraction:**
   - Separate **Radar Backscatter Change** (physical measurement) from **Environmental Interpretation** (hypothesis).
   - Implement a statistical 5-tier change model based on the filtered noise standard deviation ($\sigma_{\text{filtered}} \approx 1.2\text{ dB}$):
     - Significant Decrease ($< -2.5\text{ dB}$)
     - Moderate Decrease ($-2.5\text{ dB}$ to $-1.2\text{ dB}$)
     - Stable ($\pm 1.2\text{ dB}$)
     - Moderate Increase ($+1.2\text{ dB}$ to $+2.5\text{ dB}$)
     - Significant Increase ($> +2.5\text{ dB}$)
   - Apply Connected-Component Region Extraction (MMU $\ge 20$ pixels / $2,000\text{ m}^2$) to delineate spatially coherent change zones and export as interactive GeoJSON vector features.
3. **Phase 4 & 5 — Interactive UI Redesign:**
   - **Multi-View Navigation:**
     1. *Overview*: AOI summary, timeline, key findings.
     2. *Observations*: Raw vs. Filtered toggle, polarization selector, opacity slider.
     3. *Swipe Comparison*: Interactive before/after split-screen swipe tool.
     4. *Environmental Change Map*: Vector change regions with click-to-inspect feature popup (area, mean $\Delta\text{dB}$, confidence, interpretation).
     5. *Analysis / ML*: Separate layers for statistical change vs. unsupervised clustering ($k=4$).
     6. *Scientific Reports*: Export and view technical documentation.
4. **Phase 6 & 7 — Scientific Dashboard & ML Integration:**
   - Recharts graphs with error bars ($\pm 1\sigma$), measurement units, and contextual interpretation.
   - Maintain clear separation between ML clusters and measured differences.

---

## 6. Files Requiring Modification

- `backend/main.py`: Add filtering pipeline, vector polygonization endpoint, GeoJSON region delivery, and filtered layer endpoints.
- `ml_engine/run_ml.py`: Update to support filtered feature inputs and region statistics.
- `frontend/src/types.ts`: Add data structures for vector change regions, swipe modes, and filtered layers.
- `frontend/src/components/MapView.tsx`: Implement swipe comparison view, vector change polygon overlays, and click-inspector popups.
- `frontend/src/components/ControlPanel.tsx`: Add navigation tabs (Overview, Observations, Swipe, Change Map, ML, Reports).
- `frontend/src/components/StatsDashboard.tsx`: Enhance with standard deviations, confidence intervals, and explanatory tooltips.
