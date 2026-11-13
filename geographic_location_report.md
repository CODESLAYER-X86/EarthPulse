# NISAR GCOV Dataset Geographic Location Report

## Overview
This report details the geographical location and spatial metadata of the NISAR GCOV dataset (`Nisar.h5`) for `frequencyA`, derived via programmatic inspection using `pyproj` and `h5py`.

## Coordinate Reference System (CRS)
- **EPSG Code:** `EPSG:32725`
- **Projection Name:** WGS 84 / UTM Zone 25S
- **Units:** Meters

## Projected Coordinates
- **X Range (Easting):** 116,645.0 m to 449,995.0 m
- **Y Range (Northing):** 9,055,445.0 m to 9,380,155.0 m
- **Pixel Spacing:** 10.0 m (X and Y)

## Geographic Bounding Box (WGS84)
Using `pyproj` to transform the projected UTM Zone 25S boundary coordinates to geographic coordinates (EPSG:4326):
- **Minimum Latitude:** -8.5448° (approx. 8° 32' 41" S)
- **Maximum Latitude:** -5.5975° (approx. 5° 35' 51" S)
- **Minimum Longitude:** -36.4813° (approx. 36° 28' 53" W)
- **Maximum Longitude:** -33.4515° (approx. 33° 27' 06" W)

## Geographic Center
- **Latitude:** -7.0723° S
- **Longitude:** -34.9617° W

## Regional Context
The bounding box places this NISAR scene in **Eastern Brazil**, covering coastal and inland sections of the Northeast region (primarily encompassing parts of Paraíba, Pernambuco, and surrounding areas).

## Verification
- Coordinates and projection parameters were extracted directly from `/science/LSAR/GCOV/grids/frequencyA/xCoordinates`, `yCoordinates`, and `projection`.
- Verified consistency against the spatial reference and transform metadata embedded in the previously exported subset (`frequencyA_subset.tif`).
