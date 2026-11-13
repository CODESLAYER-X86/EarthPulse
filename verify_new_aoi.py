import h5py
import numpy as np

# Sites found in previous run
# Site 1: Row=1765, Col=13572
# Site 2: Row=1715, Col=13975
sites = [
    (1765, 13572),
    (1715, 13975)
]

# Proposed new AOI
start_row, end_row = 1600, 2100
start_col, end_col = 13500, 14000

print(f"Testing AOI: Rows {start_row}:{end_row}, Cols {start_col}:{end_col}")

for i, (r, c) in enumerate(sites):
    contained_r = start_row <= r < end_row
    contained_c = start_col <= c < end_col
    print(f"Site {i+1} (Row={r}, Col={c}) contained: {contained_r and contained_c}")
