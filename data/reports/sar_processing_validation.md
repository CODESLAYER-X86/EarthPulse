# SAR Processing & Speckle Reduction Validation Report
**Project:** Dancing with SARs — NISAR L2 GCOV Temporal Environmental Analysis  
**Study Area:** Potengi Estuary, Natal, Brazil (EPSG:32725)  
**Deliverable:** `data/reports/sar_processing_validation.md`  
**Date:** 2026-11-11  

---

## 1. SAR Preprocessing Methodology
- **Input Product:** Calibrated Gamma-Zero ($\gamma^0$) linear power from NISAR L2 GCOV Frequency A.
- **Adaptive Filtering:** Enhanced Lee Speckle Filter operating strictly in the linear intensity domain ($5\times 5$ moving kernel, nominal $\text{ENL} = 1.7$).
- **Decibel Conversion:** $\gamma^0_{\text{filtered, dB}} = 10 \log_{10}(\gamma^0_{\text{filtered, linear}})$ for valid pixels.
- **Preservation Principle:** Raw linear observations in `data/processed/` are preserved unmodified. Filtered outputs are stored in `data/filtered/`.

---

## 2. Speckle Suppression & Noise Metrics

| Target Area | Raw ENL | Filtered ENL | Speckle Variance Reduction |
| :--- | :---: | :---: | :---: |
| **Open Water / Estuary Channel** | 1.60 | 4.27 | 62.5% reduction |
| **Mangrove Canopy (Volume Scattering)** | 2.04 | 4.81 | 57.6% reduction |

- **Edge Preservation:** The local variation coefficient $C_i$ switches weighting to original pixel intensities over point targets and riverbanks ($C_i \ge C_{\max}$), preventing boundary blurring.
- **Noise Floor:** Standard deviation of pairwise difference dropped from **2.86 dB down to 1.30 dB**.

---

## 3. Pairwise Temporal Difference Quality Metrics

| Pair / Polarization | Mean $\Delta\text{dB}$ | Median $\Delta\text{dB}$ | Std $\Delta\text{dB}$ | IQR (dB) | Stable ($\pm 1.25\text{dB}$) | Sig Change ($> 2.5\text{dB}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Aug 22 → Oct 09 (HH)** | 0.02 | 0.03 | 1.35 | 1.31 | 78.1% | 4.7% |
| **Oct 09 → Oct 21 (HH)** | -0.07 | -0.07 | 1.25 | 1.21 | 80.2% | 4.0% |
| **Aug 22 → Oct 21 (Full 60-day) (HH)** | -0.05 | -0.05 | 1.30 | 1.18 | 81.7% | 4.0% |
| **Aug 22 → Oct 09 (HV)** | 0.66 | 0.64 | 1.38 | 1.39 | 67.0% | 7.4% |
| **Oct 09 → Oct 21 (HV)** | -0.03 | -0.03 | 1.20 | 1.15 | 81.9% | 3.9% |
| **Aug 22 → Oct 21 (Full 60-day) (HV)** | 0.64 | 0.61 | 1.34 | 1.30 | 70.0% | 6.1% |

---

## 4. Scientific Conclusion
Enhanced Lee filtering in the linear intensity domain successfully suppressed single-look speckle noise while maintaining the sharp coastal boundaries of the Potengi Estuary. Pairwise differences computed on filtered data reflect genuine surface radiometric shifts rather than Rayleigh fading noise.
