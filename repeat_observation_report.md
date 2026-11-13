# NISAR Repeat Observation Report

## Overview
This report identifies confirmed repeat NISAR GCOV observations for the study of coastal wetland and mangrove changes in Northeastern Brazil. The target granule is:
`NISAR_L2_PR_GCOV_033_139_D_050_0005_NASV_A_20261021T201350_20261021T201413_P05023_N_P_J_001`

## Parameters
- **Relative Orbit:** 139
- **Frame:** 050

## Search Methodology
The search was performed using the `asf_search` Python package to query the NASA Central Metadata Repository (CMR). The query criteria included platform `NISAR`, processing level `GCOV`, relative orbit `139`, and frame `50`.

The search returned three confirmed granules (cycles 031, 032, and 033). These granules were verified to have matching spatial footprints and are suitable for repeat observation analysis. Note: The catalogue lists these as `ASCENDING`, despite the `_D_` in the original granule name.

## Confirmed Repeat Observations

| Granule Filename | Acquisition Date | Cycle | Orbit | Frame | Direction | Freq/Pol | Version | Frame Cov | Download Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| NISAR_L2_PR_GCOV_031_139_D_050_... | 2026-09-27 | 031 | 139 | 050 | ASC | L-band/VV | P05023 | Partial | [Download](https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_031_139_D_050_0005_NASV_A_20260927T201350_20260927T201412_P05023_N_P_J_001/NISAR_L2_PR_GCOV_031_139_D_050_0005_NASV_A_20260927T201350_20260927T201412_P05023_N_P_J_001.h5) |
| NISAR_L2_PR_GCOV_032_139_D_050_... | 2026-10-09 | 032 | 139 | 050 | ASC | L-band/VV | P05023 | Partial | [Download](https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_032_139_D_050_0005_NASV_A_20261009T201350_20261009T201413_P05023_N_P_J_001/NISAR_L2_PR_GCOV_032_139_D_050_0005_NASV_A_20261009T201350_20261009T201413_P05023_N_P_J_001.h5) |
| NISAR_L2_PR_GCOV_033_139_D_050_... | 2026-10-21 | 033 | 139 | 050 | ASC | L-band/VV | P05023 | Partial | [Download](https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_PROVISIONAL_V1/NISAR_L2_PR_GCOV_033_139_D_050_0005_NASV_A_20261021T201350_20261021T201413_P05023_N_P_J_001/NISAR_L2_PR_GCOV_033_139_D_050_0005_NASV_A_20261021T201350_20261021T201413_P05023_N_P_J_001.h5) |

## Summary
These three granules represent confirmed, compatible repeat observations. They share identical geometry, frame coverage (Partial), and polarization (VV), making them ideal for long-term monitoring of coastal wetlands and mangroves in Northeastern Brazil.
