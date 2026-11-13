# NISAR Data Contract — Dancing with SARs

## 1. Study Area & Spatial Reference
- **Name:** Potengi Estuary, Natal, Rio Grande do Norte, Brazil
- **CRS:** `EPSG:32725` (WGS 84 / UTM zone 25S)
- **Raster Dimensions:** 500 rows × 500 columns (250,000 pixels)
- **Pixel Spacing:** 10.0 m × 10.0 m
- **Coverage Area:** 25.0 km²
- **Affine Transform:** `[10.0, 0.0, 251880.0, 0.0, -10.0, 9365260.0, 0.0, 0.0, 1.0]`
- **NoData Value:** `-9999.0` (for float rasters), `0` (for uint8 masks)

---

## 2. Acquisitions & Products
- **Product:** NISAR L2 GCOV (Geocoded Polarimetric Covariance), Frequency A
- **Cycle 028:** 2026-08-22 (`data/processed/cycle_028/`)
- **Cycle 032:** 2026-10-09 (`data/processed/cycle_032/`)
- **Cycle 033:** 2026-10-21 (`data/processed/cycle_033/`)

---

## 3. Band Specifications & Value Ranges
- **Linear Backscatter:** Calibrated gamma-zero power ($\gamma^0_{\text{linear}} > 0$).
- **Decibel (dB):** $\gamma^0_{\text{dB}} = 10 \cdot \log_{10}(\gamma^0_{\text{linear}})$.
- **Validity Mask:** 1 = Valid radar sample, 0 = Invalid/Fill.

---

## 4. Frozen 12-Band ML Feature Stack (`data/ml/feature_stack.tif`)
The multi-band GeoTIFF contains exactly 12 bands in the following order:

| Band Index | Feature Name | Description | Units |
| :---: | :--- | :--- | :--- |
| 1 | `hh_028_db` | Cycle 028 HH backscatter | dB |
| 2 | `hh_032_db` | Cycle 032 HH backscatter | dB |
| 3 | `hh_033_db` | Cycle 033 HH backscatter | dB |
| 4 | `hv_028_db` | Cycle 028 HV backscatter | dB |
| 5 | `hv_032_db` | Cycle 032 HV backscatter | dB |
| 6 | `hv_033_db` | Cycle 033 HV backscatter | dB |
| 7 | `hh_diff_028_032` | $\text{HH}_{032} - \text{HH}_{028}$ | dB |
| 8 | `hh_diff_032_033` | $\text{HH}_{033} - \text{HH}_{032}$ | dB |
| 9 | `hh_diff_028_033` | $\text{HH}_{033} - \text{HH}_{028}$ | dB |
| 10 | `hv_diff_028_032` | $\text{HV}_{032} - \text{HV}_{028}$ | dB |
| 11 | `hv_diff_032_033` | $\text{HV}_{033} - \text{HV}_{032}$ | dB |
| 12 | `hv_diff_028_033` | $\text{HV}_{033} - \text{HV}_{028}$ | dB |

---

## 5. Temporal Difference Products (`data/temporal/`)
- `HH_diff_028_032.tif`
- `HH_diff_032_033.tif`
- `HH_diff_028_033.tif`
- `HV_diff_028_032.tif`
- `HV_diff_032_033.tif`
- `HV_diff_028_033.tif`
- `common_valid_mask.tif` (1 = valid across all three dates, 0 = invalid in at least one)
