import h5py
import numpy as np

files = [
    ("Cycle 028", "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"),
    ("Cycle 032", "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"),
    ("Cycle 033", "Nisar.h5")
]

# Load coordinates once
with h5py.File(files[0][1], 'r') as f:
    xc = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    yc = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]

# Define candidate centers (UTM Zone 25S)
# Bounds: x: 116,645.0 to 449,995.0; y: 9,055,445.0 to 9,380,155.0
candidates = {
    "Candidate 1 (Rio Preguicas)": (300000, 9200000),
    "Candidate 2 (Western Mangroves)": (200000, 9150000),
    "Candidate 3 (Eastern Mangroves)": (400000, 9300000)
}

def get_valid_stats(f_paths, center_x, center_y, size=500):
    # Find indices
    col_idx = np.abs(xc - center_x).argmin()
    row_idx = np.abs(yc - center_y).argmin()
    
    # Define window
    r_start, r_end = row_idx - size//2, row_idx + size//2
    c_start, c_end = col_idx - size//2, col_idx + size//2
    
    valid_mask = np.ones((size, size), dtype=bool)
    
    for _, fp in f_paths:
        with h5py.File(fp, 'r') as f:
            mask = f['science/LSAR/GCOV/grids/frequencyA/mask'][r_start:r_end, c_start:c_end]
            hh = f['science/LSAR/GCOV/grids/frequencyA/HHHH'][r_start:r_end, c_start:c_end]
            hv = f['science/LSAR/GCOV/grids/frequencyA/HVHV'][r_start:r_end, c_start:c_end]
            
            # Valid per date
            date_valid = (mask >= 1) & (mask <= 254) & np.isfinite(hh) & (hh > 0) & np.isfinite(hv) & (hv > 0)
            valid_mask &= date_valid
            
    return np.sum(valid_mask) / (size * size)

print("Evaluating Candidates...")
for name, (x, y) in candidates.items():
    pct = get_valid_stats(files, x, y)
    print(f"{name}: Common-valid percentage = {pct*100:.2f}%")
