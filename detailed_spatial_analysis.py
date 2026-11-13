import h5py
import numpy as np
import hashlib

files = [
    ("Cycle 028", "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"),
    ("Cycle 032", "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"),
    ("Cycle 033", "Nisar.h5")
]

print("=== STEP 3: Coordinate Array Verification ===")
coord_hashes = {}
coord_arrays = {}

for name, fp in files:
    with h5py.File(fp, 'r') as f:
        xc = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
        yc = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]
        
        xc_hash = hashlib.sha256(xc.tobytes()).hexdigest()
        yc_hash = hashlib.sha256(yc.tobytes()).hexdigest()
        
        coord_hashes[name] = (xc_hash, yc_hash)
        coord_arrays[name] = (xc, yc)
        print(f"{name}: xCoordinates shape {xc.shape}, hash {xc_hash[:12]}... | yCoordinates shape {yc.shape}, hash {yc_hash[:12]}...")

xc_028, yc_028 = coord_arrays["Cycle 028"]
xc_032, yc_032 = coord_arrays["Cycle 032"]
xc_033, yc_033 = coord_arrays["Cycle 033"]

x_eq_032 = np.array_equal(xc_028, xc_032)
y_eq_032 = np.array_equal(yc_028, yc_032)
x_eq_033 = np.array_equal(xc_028, xc_033)
y_eq_033 = np.array_equal(yc_028, yc_033)

print(f"Cycle 028 vs 032: xCoordinates identical: {x_eq_032}, yCoordinates identical: {y_eq_032}")
print(f"Cycle 028 vs 033: xCoordinates identical: {x_eq_033}, yCoordinates identical: {y_eq_033}")


print("\n=== STEP 2: Exact Common Coverage Calculation (Windowed Processing) ===")
# Open all three files
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

valid_all_3 = 0
valid_exactly_2 = 0
valid_exactly_1 = 0
invalid_all_3 = 0
footprint_pixels = 0 # non-fill in all or any? Let's define footprint as pixels where at least one granule is not fill (or acquisition extent)

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
    
    # Valid condition per date: mask 1-254 AND finite positive HH and HV
    v_cond_1 = (m1 >= 1) & (m1 <= 254) & np.isfinite(h1) & (h1 > 0) & np.isfinite(v1) & (v1 > 0)
    v_cond_2 = (m2 >= 1) & (m2 <= 254) & np.isfinite(h2) & (h2 > 0) & np.isfinite(v2) & (v2 > 0)
    v_cond_3 = (m3 >= 1) & (m3 <= 254) & np.isfinite(h3) & (h3 > 0) & np.isfinite(v3) & (v3 > 0)
    
    inv_cond_1 = (m1 == 0)
    inv_cond_2 = (m2 == 0)
    inv_cond_3 = (m3 == 0)
    
    sum_valid = v_cond_1.astype(int) + v_cond_2.astype(int) + v_cond_3.astype(int)
    
    valid_all_3 += np.sum(sum_valid == 3)
    valid_exactly_2 += np.sum(sum_valid == 2)
    valid_exactly_1 += np.sum(sum_valid == 1)
    
    invalid_all_3 += np.sum(inv_cond_1 & inv_cond_2 & inv_cond_3)
    
    # Footprint: pixels that are not fill (mask != 255) across acquisition extent (e.g. in at least one granule or all)
    # Let's define geographic footprint as union of valid/invalid (mask != 255) in all three or intersection
    not_fill = (m1 != 255) | (m2 != 255) | (m3 != 255)
    footprint_pixels += np.sum(not_fill)

f028.close()
f032.close()
f033.close()

print(f"Total pixels: {total_pixels}")
print(f"Geographic footprint pixels (non-fill in at least one): {footprint_pixels} ({footprint_pixels/total_pixels*100:.2f}%)")
print(f"Valid in all 3 cycles (with finite positive HH/HV): {valid_all_3}")
print(f"  -> Relative to full grid: {valid_all_3/total_pixels*100:.2f}%")
print(f"  -> Relative to geographic footprint: {valid_all_3/footprint_pixels*100:.2f}%")
print(f"Valid in exactly 2 cycles: {valid_exactly_2} ({valid_exactly_2/total_pixels*100:.2f}%)")
print(f"Valid in exactly 1 cycle: {valid_exactly_1} ({valid_exactly_1/total_pixels*100:.2f}%)")
print(f"Invalid in all 3 cycles (mask == 0): {invalid_all_3} ({invalid_all_3/total_pixels*100:.2f}%)")

print("\n=== STEP 4: Generating Lightweight Previews ===")
# Generate a downsampled preview (e.g. every 64th pixel) and save summary stats / preview array
f028 = h5py.File(files[0][1], 'r')
m028_ds = f028['science/LSAR/GCOV/grids/frequencyA/mask'][::64, ::64]
f028.close()

np.save('/tmp/opencode/preview_mask_028_ds.npy', m028_ds)
print("Saved downsampled preview to /tmp/opencode/preview_mask_028_ds.npy (shape:", m028_ds.shape, ")")
