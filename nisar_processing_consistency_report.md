# NISAR Processing Consistency Report

## 1. Objective
To assess the consistency of NISAR L2 GCOV observations across cycles 028, 032, and 033 for temporal analysis, specifically investigating potential processing version discrepancies (PGE R05.02.3 vs. R05.03.2).

## 2. Dataset Availability
A search of available candidate granules reveals the following version distribution:

| Cycle | Date | Granule ID | PGE Version |
| :--- | :--- | :--- | :--- |
| 028 | 2026-08-22 | `NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001` | R05.02.3 |
| 032 | 2026-10-09 | `NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001` | R05.02.3 |
| 033 | 2026-10-21 | `NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05023_N_F_J_001` | R05.02.3 |
| 033 | 2026-10-21 | `NISAR_L2_PR_GCOV_033_139_D_092_4005_DHDH_A_20261021T203740_20261021T203818_P05036_N_F_J_001` | R05.03.2 |

Alternative processing versions (R05.03.2) do not exist for cycles 028 and 032 within the available dataset.

## 3. Findings & Investigation
*   **Version Distribution:** Cycles 028 and 032 are exclusively available in PGE R05.02.3. Cycle 033 is available in both R05.02.3 and R05.03.2.
*   **Processing Differences:** The change from R05.02.3 to R05.03.2 indicates an update in the Product Generation Executive (PGE). Without official release notes detailing specific changes to GCOV calibration algorithms, we assume these are minor improvements.
*   **Comparison Impact:** Using R05.02.3 for all three cycles (028, 032, 033) ensures processing consistency.

## 4. Recommendation
**Selection: A. Three observations with identical processing versions.**

By selecting the R05.02.3 version for Cycle 033, we ensure that all three observations (028, 032, and 033) are processed with the same version (PGE R05.02.3), eliminating potential discrepancies introduced by the PGE upgrade to R05.03.2.

