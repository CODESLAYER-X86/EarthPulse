import h5py
import numpy as np

files = [
    ("Cycle 028", "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"),
    ("Cycle 032", "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"),
    ("Cycle 033", "Nisar.h5")
]

with h5py.File(files[0][1], 'r') as f:
    xc = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    yc = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]

candidates = {
    "candidate_1_preguicas": (300000, 9200000),
    "candidate_2_western": (200000, 9150000),
    "candidate_3_eastern": (400000, 9300000)
}

for name, (cx, cy) in candidates.items():
    col_idx = np.abs(xc - cx).argmin()
    row_idx = np.abs(yc - cy).argmin()
    size = 500
    r_start, r_end = row_idx - size//2, row_idx + size//2
    c_start, c_end = col_idx - size//2, col_idx + size//2
    
    with h5py.File(files[0][1], 'r') as f:
        m = f['science/LSAR/GCOV/grids/frequencyA/mask'][r_start:r_end, c_start:c_end]
        np.save(f'/tmp/opencode/{name}_mask_028.npy', m)
        
print("Saved candidate previews to /tmp/opencode/")
