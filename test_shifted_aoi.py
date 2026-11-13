import h5py
import numpy as np
from pyproj import Transformer

# Mangrove sites
mangrove_sites = [
    (-5.763056, -35.236111),
    (-5.758611, -35.199722)
]

transformer = Transformer.from_crs("EPSG:4326", "EPSG:32725", always_xy=True)
file_path = "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"

with h5py.File(file_path, 'r') as f:
    x_coords = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    y_coords = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]
    
    freqA = f['science/LSAR/GCOV/grids/frequencyA']
    hh = freqA['HHHH'][:]
    hv = freqA['HVHV'][:]
    print("HHHH shape:", hh.shape, "HVHV shape:", hv.shape)

# Shifted AOI: 500x500 pixels containing both mangrove sites
# Row range: 1490 to 1990, Col range: 13523 to 14023
row_start, row_end = 1490, 1990
col_start, col_end = 13523, 14023

print(f"Shifted AOI Windows:")
print(f"  Rows: {row_start}:{row_end} ({row_end - row_start} pixels)")
print(f"  Cols: {col_start}:{col_end} ({col_end - col_start} pixels)")
print(f"  Easting range: {x_coords[col_start]:.2f} to {x_coords[col_end-1]:.2f} m")
print(f"  Northing range: {y_coords[row_end-1]:.2f} to {y_coords[row_start]:.2f} m")

for i, (lat, lon) in enumerate(mangrove_sites):
    easting, northing = transformer.transform(lon, lat)
    col_idx = (np.abs(x_coords - easting)).argmin()
    row_idx = (np.abs(y_coords - northing)).argmin()
    in_aoi = (row_start <= row_idx < row_end) and (col_start <= col_idx < col_end)
    print(f"Mangrove Site {i+1} (Row={row_idx}, Col={col_idx}): Inside Shifted AOI? {in_aoi}")

# Calculate finite-positive coverage for HHHH and HVHV in this window
hh_sub = hh[row_start:row_end, col_start:col_end]
hv_sub = hv[row_start:row_end, col_start:col_end]

total_pixels = 500 * 500
hh_valid = np.isfinite(hh_sub) & (hh_sub > 0)
hv_valid = np.isfinite(hv_sub) & (hv_sub > 0)
common_valid = hh_valid & hv_valid

print(f"Coverage Analysis for Shifted AOI:")
print(f"  Total pixels: {total_pixels}")
print(f"  HHHH finite-positive pixels: {hh_valid.sum()} ({hh_valid.sum()/total_pixels*100:.2f}%)")
print(f"  HVHV finite-positive pixels: {hv_valid.sum()} ({hv_valid.sum()/total_pixels*100:.2f}%)")
print(f"  Common valid (HHHH & HVHV) pixels: {common_valid.sum()} ({common_valid.sum()/total_pixels*100:.2f}%)")
