import h5py
import numpy as np

files = {
    'Cycle 028': 'data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5',
    'Cycle 032': 'data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5',
    'Cycle 033': 'Nisar.h5'
}

for name, path in files.items():
    print(f"=== {name} ({path}) ===")
    with h5py.File(path, 'r') as f:
        g = f['science/LSAR/GCOV/grids/frequencyA']
        print(f"  xCoordinates shape: {g['xCoordinates'].shape}, min: {g['xCoordinates'][0]}, max: {g['xCoordinates'][-1]}")
        print(f"  yCoordinates shape: {g['yCoordinates'].shape}, min: {g['yCoordinates'][-1]}, max: {g['yCoordinates'][0]}") # y usually descending
        print(f"  xCoordinateSpacing: {g['xCoordinateSpacing'][()]}")
        print(f"  yCoordinateSpacing: {g['yCoordinateSpacing'][()]}")
        proj_ds = g['projection']
        if proj_ds.dtype.names is not None:
            print(f"  Projection attributes/fields: {proj_ds.dtype.names}")
            for field in proj_ds.dtype.names:
                print(f"    {field}: {proj_ds[...][field]}")
        else:
            print(f"  Projection value: {proj_ds[()]}")
        
        # Check attributes on projection or grid
        for k, v in g.attrs.items():
            print(f"  Attr {k}: {v}")
