import h5py
import numpy as np

def calculate_coverage(file_path):
    print(f"Analyzing: {file_path}")
    with h5py.File(file_path, 'r') as f:
        mask_dset = f['science/LSAR/GCOV/grids/frequencyA/mask']
        total_pixels = mask_dset.shape[0] * mask_dset.shape[1]
        
        fill_count = 0
        invalid_count = 0
        valid_count = 0
        
        chunk_size = 1000
        for i in range(0, mask_dset.shape[0], chunk_size):
            chunk = mask_dset[i:i+chunk_size, :]
            fill_count += np.sum(chunk == 255)
            invalid_count += np.sum(chunk == 0)
            valid_count += np.sum((chunk >= 1) & (chunk <= 254))
            
        return total_pixels, invalid_count, fill_count, valid_count

file_paths = [
    ("Cycle 028", "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"),
    ("Cycle 032", "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"),
    ("Cycle 033", "Nisar.h5")
]

for name, fp in file_paths:
    total, invalid, fill, valid = calculate_coverage(fp)
    print(f"Results for {name} ({fp}):")
    print(f"  Total pixels: {total}")
    print(f"  Invalid (mask == 0): {invalid} ({invalid/total*100:.2f}%)")
    print(f"  Fill (mask == 255): {fill} ({fill/total*100:.2f}%)")
    print(f"  Valid (mask 1-254): {valid} ({valid/total*100:.2f}%)")
    print("-" * 40)
