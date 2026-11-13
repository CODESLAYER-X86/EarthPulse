# NISAR GCOV Inspection Report

## Overview
This report documents the inspection of the NISAR GCOV HDF5 file (`Nisar.h5`). The analysis was performed using a Python 3.12 environment with `numpy` 2.5.4 and `h5py` 3.16.0.

## Dataset Inspection
The NISAR GCOV product contains two frequency bands (`frequencyA` and `frequencyB`). The datasets are structured in a consistent grid.

### Key Datasets Summary
| Dataset | Frequency A Shape | Frequency B Shape | Dtype | Description |
| :--- | :--- | :--- | :--- | :--- |
| `HHHH` | (32472, 33336) | (4059, 4167) | float32 | Geocoded polarimetric covariance term HHHH |
| `HVHV` | (32472, 33336) | (4059, 4167) | float32 | Geocoded polarimetric covariance term HVHV |
| `mask` | (32472, 33336) | (4059, 4167) | uint8 | Valid samples subswath mask |
| `numberOfLooks` | (32472, 33336) | (4059, 4167) | float32 | Number of radar looks |

## Geospatial Metadata
- **Projection:** Transverse Mercator (UTM Zone 25S, EPSG: 32725)
- **Ellipsoid:** WGS84
- **Coordinates:** X and Y coordinates are provided in meters.
- **Pixel Spacing:** Derived from `xCoordinateSpacing` and `yCoordinateSpacing` (verified as 10m based on GeoTIFF export).

## Visualization and Subset Extraction
A 1024x1024 subset was extracted to analyze the data without loading the full 1GB+ arrays into memory.
- **Preview:** `frequencyA_preview.png` displays HHHH (dB), HVHV (dB), and the quality mask.
- **Subset Export:** `frequencyA_subset.tif` was exported as a 3-band GeoTIFF (HHHH, HVHV, Mask) with proper CRS and transformation.

## Observations
- **Data Values:** The datasets represent linear power (gamma0 or sigma0). Decibel conversion ($10 \cdot \log_{10}(x)$) is required for visualization.
- **Masking:** Valid pixels have mask values other than 255 (the fill value).
- **Quality:** The subset inspection indicates valid data coverage within the examined region.

## Files Generated
- `inspection_report.md` (this file)
- `frequencyA_preview.png`
- `frequencyA_subset.tif`
- `inspect_data.py` (inspection script)
- `process_subset.py` (extraction script)
