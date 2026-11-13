import h5py
import numpy as np

files = {
    "Cycle 028": "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5",
    "Cycle 032": "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5",
    "Cycle 033": "Nisar.h5"
}

for name, path in files.items():
    print(f"=== {name} ({path}) ===")
    with h5py.File(path, 'r') as f:
        g = f['/science/LSAR/GCOV/grids/frequencyA']
        print("  Shape:", f['/science/LSAR/GCOV/grids/frequencyA/HHHH'].shape)
        print("  xSpacing:", g['xCoordinateSpacing'][()])
        print("  ySpacing:", g['yCoordinateSpacing'][()])
        x_coords = g['xCoordinates']
        y_coords = g['yCoordinates']
        print("  xBounds:", x_coords[0], x_coords[-1])
        print("  yBounds:", y_coords[0], y_coords[-1])
        proj = g['projection'][()]
        print("  Projection:", proj)
        # Check if mask exists and get valid percentage
        if 'mask' in g:
            mask = g['mask'][:]
            # Usually 0 is valid or non-zero is valid, let's check unique values
            print("  Mask unique values:", np.unique(mask[:100, :100]))
