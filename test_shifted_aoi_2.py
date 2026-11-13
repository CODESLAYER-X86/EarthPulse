import h5py
import numpy as np

file_path = "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"

row_start, row_end = 1490, 1990
col_start, col_end = 13524, 14024

with h5py.File(file_path, 'r') as f:
    freqA = f['science/LSAR/GCOV/grids/frequencyA']
    
    # Read HHHH and HVHV subset
    # Note: GCOV datasets are usually (y, x) or (row, col)
    hhhh = freqA['HHHH'][row_start:row_end, col_start:col_end]
    hvhv = freqA['HVHV'][row_start:row_end, col_start:col_end]
    
    x_coords = freqA['xCoordinates'][col_start:col_end]
    y_coords = freqA['yCoordinates'][row_start:row_end]

print(f"Window: Rows {row_start}:{row_end}, Cols {col_start}:{col_end}")
print(f"Shape: {hhhh.shape}")
print(f"X range: {x_coords[0]} to {x_coords[-1]}")
print(f"Y range: {y_coords[0]} to {y_coords[-1]}")

# Check valid pixels (finite and positive, or non-zero)
hhhh_valid = np.isfinite(hhhh) & (hhhh > 0)
hvhv_valid = np.isfinite(hvhv) & (hvhv > 0)
common_valid = hhhh_valid & hvhv_valid

total_pixels = hhhh.size
hhhh_count = np.sum(hhhh_valid)
hvhv_count = np.sum(hvhv_valid)
common_count = np.sum(common_valid)

print(f"Total pixels: {total_pixels}")
print(f"HHHH valid: {hhhh_count} ({hhhh_count/total_pixels*100:.2f}%)")
print(f"HVHV valid: {hvhv_count} ({hvhv_count/total_pixels*100:.2f}%)")
print(f"Common valid: {common_count} ({common_count/total_pixels*100:.2f}%)")
