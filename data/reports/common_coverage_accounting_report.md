# Common Coverage Accounting Report

## 1. Pixel Classification Summary

The total raster grid size is 1,082,486,592 pixels. The following table provides a mutually exclusive classification of all pixels within this grid based on their validity across the three NISAR GCOV cycles (028, 032, and 033).

A pixel is considered "Valid" if and only if it has a mask value between 1 and 254 AND contains finite, positive backscatter values for both HH and HV polarizations.

| Classification Category | Pixel Count | % of Total |
| :--- | :--- | :--- |
| **Valid in all 3 cycles** | 630,673,082 | 58.26% |
| **Valid in exactly 2 cycles** | 4,585,959 | 0.42% |
| **Valid in exactly 1 cycle** | 2,219,120 | 0.21% |
| **Invalid (Valid in 0 cycles)** | 445,008,431 | 41.11% |
| **Total** | 1,082,486,592 | 100.00% |

## 2. Detailed Breakdown of Invalid Pixels (Valid in 0 cycles)

The 445,008,431 pixels classified as "Invalid" are further categorized as follows:

| Invalid Category | Pixel Count |
| :--- | :--- |
| **All 3 cycles are Fill (255)** | 416,028,481 |
| **All 3 cycles are Invalid Radar Sample (0)** | 25,820,671 |
| **Other (Mixed Fill, Invalid, or No-Data)** | 3,159,279 |
| **Total** | 445,008,431 |

This exhaustive accounting demonstrates that the vast majority of non-valid pixels are simply outside the NISAR acquisition footprint (Fill), with a smaller subset of pixels specifically classified as invalid radar samples.
