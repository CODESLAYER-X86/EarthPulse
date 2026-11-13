import h5py
import os

files = {
    "Cycle 028": "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5",
    "Cycle 032": "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5",
    "Cycle 033": "Nisar.h5"
}

def inspect_file(name, path):
    print(f"=== {name} ({path}) ===")
    if not os.path.exists(path):
        print("  FILE NOT FOUND")
        return
    try:
        with h5py.File(path, 'r') as f:
            print(f"  File size: {os.path.getsize(path)}")
            print("  Keys:", list(f.keys()))
            if 'identification' in f:
                ident = f['identification']
                print("  Identification keys:", list(ident.keys()))
            else:
                print("  'identification' group not found.")
    except Exception as e:
        print(f"  Error reading HDF5: {e}")

for name, path in files.items():
    inspect_file(name, path)
