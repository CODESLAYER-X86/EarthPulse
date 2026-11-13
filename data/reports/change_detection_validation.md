# Environmental Change Detection & Region Extraction Report
**Project:** Dancing with SARs — NISAR L2 GCOV Temporal Analysis  
**Study Area:** Potengi Estuary, Natal, Brazil  
**Deliverable:** `data/reports/change_detection_validation.md`  
**Date:** 2026-11-11  

---

## 1. Classification Framework
To prevent random speckle fluctuations from masquerading as environmental change, a 5-tier classification model based on the empirical filtered noise floor ($\sigma_{\text{filtered}} = 1.25\text{ dB}$) is established:

1. **Significant Decrease ($< -2.50\text{ dB}$, $> 2\sigma$):** High confidence of reduced backscatter (e.g. tidal inundation, wetland flooding, or canopy loss).
2. **Moderate Decrease ($-2.50\text{ dB}$ to $-1.25\text{ dB}$, $1-2\sigma$):** Moderate confidence of surface moisture increase or partial defoliation.
3. **Stable Area ($-1.25\text{ dB}$ to $+1.25\text{ dB}$, $\pm 1\sigma$):** Radiometrically stable within sensor noise tolerances.
4. **Moderate Increase ($+1.25\text{ dB}$ to $+2.50\text{ dB}$, $1-2\sigma$):** Moderate confidence of surface drying or seasonal foliage increase.
5. **Significant Increase ($> +2.50\text{ dB}$, $> 2\sigma$):** High confidence of structural change or increased double-bounce reflectance.

---

## 2. Morphological Region Extraction (MMU $\ge 1,500\text{ m}^2$)
Individual pixel changes were filtered using binary morphological opening and connected-component labeling. Only spatially coherent patches with at least 15 contiguous pixels ($1,500\text{ m}^2$) were converted to vector polygon features.

### Extracted Region Summary:

| Interval | Polarization | Number of Coherent Change Regions | Total Change Area (ha) | GeoJSON Vector Deliverable |
| :--- | :---: | :---: | :---: | :--- |
| **Aug 22 → Oct 21** | HH | 314 regions | 92.2 ha | `data/classified/change_regions_HH_028_033.geojson` |
| **Aug 22 → Oct 21** | HV | 667 regions | 346.2 ha | `data/classified/change_regions_HV_028_033.geojson` |
| **Aug 22 → Oct 09** | HH | 477 regions | 153.2 ha | `data/classified/change_regions_HH_028_032.geojson` |
| **Aug 22 → Oct 09** | HV | 588 regions | 423.1 ha | `data/classified/change_regions_HV_028_032.geojson` |
| **Oct 09 → Oct 21** | HH | 416 regions | 153.7 ha | `data/classified/change_regions_HH_032_033.geojson` |
| **Oct 09 → Oct 21** | HV | 338 regions | 115.5 ha | `data/classified/change_regions_HV_032_033.geojson` |

---

## 3. Scientific Integrity & Attribution Note
- **Radar Measurement vs Environmental Classification:** Every extracted polygon contains its raw average decibel shift ($\Delta\text{dB}$) alongside qualified interpretation hypotheses.
- **In-Situ Requirements:** Tidal variations in the Potengi Estuary significantly alter water surface extents between high and low tide. Observed changes represent physical backscatter interactions at the satellite acquisition epoch and should not be cited as permanent mangrove deforestation without ground confirmation.
