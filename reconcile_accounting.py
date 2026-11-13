import h5py
import numpy as np

files = [
    ("Cycle 028", "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"),
    ("Cycle 032", "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"),
    ("Cycle 033", "Nisar.h5")
]

print("Starting pixel accounting reconciliation...")

f028 = h5py.File(files[0][1], 'r')
f032 = h5py.File(files[1][1], 'r')
f033 = h5py.File(files[2][1], 'r')

mask028 = f028['science/LSAR/GCOV/grids/frequencyA/mask']
mask032 = f032['science/LSAR/GCOV/grids/frequencyA/mask']
mask033 = f033['science/LSAR/GCOV/grids/frequencyA/mask']

hh028 = f028['science/LSAR/GCOV/grids/frequencyA/HHHH']
hv028 = f028['science/LSAR/GCOV/grids/frequencyA/HVHV']
hh032 = f032['science/LSAR/GCOV/grids/frequencyA/HHHH']
hv032 = f032['science/LSAR/GCOV/grids/frequencyA/HVHV']
hh033 = f033['science/LSAR/GCOV/grids/frequencyA/HHHH']
hv033 = f033['science/LSAR/GCOV/grids/frequencyA/HVHV']

nrows, ncols = mask028.shape
total_pixels = nrows * ncols

# Categories per cycle:
# 1. Fill: mask == 255
# 2. Invalid: mask == 0
# 3. Mask-Valid-But-No-Data: mask in [1, 254] AND (HH or HV not finite or <= 0)
# 4. Valid: mask in [1, 254] AND finite positive HH and HV

# Let's count mutually exclusive per-pixel combinations or aggregate counts:
# Total pixels = 1,082,486,592

valid_count_1 = 0
valid_count_2 = 0
valid_count_3 = 0

# Number of valid dates per pixel (0 to 3)
valid_dates_hist = {0: 0, 1: 0, 2: 0, 3: 0}

# For pixels with 0 valid dates, let's break down why:
# We can classify every pixel into a primary state across the 3 cycles or detailed categories.
# Let's track:
# - Valid in 3
# - Valid in 2
# - Valid in 1
# - Valid in 0:
#   - All 3 are Fill (255)
#   - All 3 are Invalid (0)
#   - All 3 are Mask-Valid-But-No-Data
#   - Mixed non-valid states (Fill, Invalid, No-Data combinations)

mixed_zero_valid = 0
all_fill = 0
all_invalid = 0
all_nodata = 0

chunk_size = 1000
for start in range(0, nrows, chunk_size):
    end = min(start + chunk_size, nrows)
    
    m1 = mask028[start:end, :]
    m2 = mask032[start:end, :]
    m3 = mask033[start:end, :]
    
    h1 = hh028[start:end, :]
    v1 = hv028[start:end, :]
    h2 = hh032[start:end, :]
    v2 = hv032[start:end, :]
    h3 = hh033[start:end, :]
    v3 = hv033[start:end, :]
    
    # Valid condition per date
    val1 = (m1 >= 1) & (m1 <= 254) & np.isfinite(h1) & (h1 > 0) & np.isfinite(v1) & (v1 > 0)
    val2 = (m2 >= 1) & (m2 <= 254) & np.isfinite(h2) & (h2 > 0) & np.isfinite(v2) & (v2 > 0)
    val3 = (m3 >= 1) & (m3 <= 254) & np.isfinite(h3) & (h3 > 0) & np.isfinite(v3) & (v3 > 0)
    
    n_valid = val1.astype(int) + val2.astype(int) + val3.astype(int)
    
    valid_dates_hist[0] += np.sum(n_valid == 0)
    valid_dates_hist[1] += np.sum(n_valid == 1)
    valid_dates_hist[2] += np.sum(n_valid == 2)
    valid_dates_hist[3] += np.sum(n_valid == 3)
    
    # Break down n_valid == 0
    zero_mask = (n_valid == 0)
    all_f = zero_mask & (m1 == 255) & (m2 == 255) & (m3 == 255)
    all_i = zero_mask & (m1 == 0) & (m2 == 0) & (m3 == 0)
    
    all_fill += np.sum(all_f)
    all_invalid += np.sum(all_i)

f028.close()
f032.close()
f033.close()

print(f"Total pixels: {total_pixels}")
print(f"Valid in 3 cycles: {valid_dates_hist[3]}")
print(f"Valid in exactly 2 cycles: {valid_dates_hist[2]}")
print(f"Valid in exactly 1 cycle: {valid_dates_hist[1]}")
print(f"Valid in 0 cycles: {valid_dates_hist[0]}")
print(f"  - All 3 fill (255): {all_fill}")
print(f"  - All 3 invalid (0): {all_invalid}")
print(f"  - Other zero-valid (mixed fill, invalid, mask-valid-no-data): {valid_dates_hist[0] - all_fill - all_invalid}")
print(f"Sum check: {sum(valid_dates_hist.values())} (Should equal {total_pixels})")
