# Spatial Validation Report: NISAR L2 GCOV (Cycles 028, 032, 033)

## 1. Spatial Validation Summary

The three NISAR L2 GCOV granules (Cycles 028, 032, and 033) were analyzed for spatial consistency and valid-pixel coverage.

### Metadata & Coordinate Comparison
All three granules exhibit identical spatial configurations:
- **Dimensions:** 32,472 (rows/y) x 33,336 (columns/x) (Total pixels: 1,082,486,592)
- **Pixel Spacing:** 10.0 meters
- **Coordinate System:** Identical CRS identified by `projection` value 32725 (UTM Zone 25S)
- **Extents:** Identical x and y coordinate ranges (x: 116,645.0 to 449,995.0; y: 9,055,445.0 to 9,380,155.0)

**Coordinate Array Verification:**
By directly hashing and comparing the `xCoordinates` and `yCoordinates` datasets across all granules:
- `xCoordinates` arrays are **100% identical** across all three cycles (SHA-256 hash prefix: `ef12534b817e...`).
- `yCoordinates` arrays are **100% identical** across all three cycles (SHA-256 hash prefix: `9ea77b2350e6...`).
- Conclusion: The granules are natively aligned at the exact pixel grid level.

### Mask Interpretation
Analysis of the `mask` dataset confirms the standard NISAR GCOV interpretation:
- `0`: Invalid radar sample (partially focused/invalid in averaging).
- `1–254`: Valid subswath identifier.
- `255`: Fill / outside radar acquisition extent.

### Individual Valid-Pixel Coverage (Frequency A)
- **Cycle 028:** 58.75% valid (635,953,794 pixels)
- **Cycle 032:** 58.80% valid (636,466,257 pixels)
- **Cycle 033:** 58.29% valid (630,990,233 pixels)

---

## 2. Multi-Temporal Common Coverage & Data Integrity

Using windowed processing (chunk size 1,000 rows) combined with finite, positive value checks for both `HHHH` and `HVHV` polarizations across all three dates, the exact common coverage was computed:

- **Geographic Footprint Pixels (non-fill in at least one cycle):** 666,458,111 (61.57% of full grid)
- **Valid in all 3 cycles (with finite positive HH/HV):** 630,673,082 pixels
  - *Relative to full grid:* **58.26%**
  - *Relative to geographic footprint:* **94.63%**
- **Valid in exactly 2 cycles:** 4,585,959 pixels (0.42%)
- **Valid in exactly 1 cycle:** 2,219,120 pixels (0.21%)
- **Invalid in all 3 cycles (mask == 0):** 25,820,671 pixels (2.39%)

---

## 3. Previews & Visualizations

Lightweight subsampled previews (downsampled by factor of 64) of the valid-pixel masks and common-valid overlap maps were successfully generated and stored in `/tmp/opencode/` without incurring high memory overhead or modifying original HDF5 files.

---

## 4. Final AOI Extraction Suitability Assessment

**Status:** **SUITABLE**
- The data is natively aligned to the exact same grid, eliminating the need for resampling, warping, or reprojection.
- High common valid-pixel coverage (~58.26% of the total grid, and 94.63% of the active acquisition footprint) ensures robust multi-temporal analysis for the target Wetland AOI.
- Original HDF5 files remain strictly unmodified.
