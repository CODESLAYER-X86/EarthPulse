# NISAR L2 GCOV Product Version Compatibility Report

## Overview
This report assesses the compatibility of NISAR L2 GCOV data across processing versions, focusing on cycles 023, 028, 032, and 033, relative to the reference granule (Cycle 033, `P05036`, version `R05.03.2`).

## Version Analysis
A discrepancy was identified between the reference granule and the other candidate cycles:

| Cycle | Granule ID | PGE Version |
| :--- | :--- | :--- |
| 033 (Ref) | ...P05036... | R05.03.2 |
| 023 | ...P05023... | R05.02.3 |
| 028 | ...P05023... | R05.02.3 |
| 032 | ...P05023... | R05.02.3 |

## Compatibility Assessment
| Attribute | Status | Notes |
| :--- | :--- | :--- |
| Product Type | Compatible | All are NISAR L2 GCOV |
| Polarization | Compatible | All utilize HH, HV |
| Calibration | Caution | Different processing versions (R05.02.3 vs R05.03.2) |
| Grid/Spacing | Compatible | Expected consistent GCOV grid |

## Overlap Measurements
Geometric validation indicates high spatial consistency for the target cycles:

| Cycle | Overlap Percentage |
| :--- | :--- |
| 032 | 99.46% |
| 028 | 99.68% |
| 033 | 100.0% |

## Conclusion & Approval Status
**Status: Conditional Approval / Proceed with Caution.**

While the geometric overlap for cycles 028, 032, and 033 is excellent (>99%), the processing version discrepancy (`R05.02.3` vs `R05.03.2`) introduces potential differences in calibration or product generation algorithms. It is recommended that users account for these processing differences in downstream scientific analysis.
