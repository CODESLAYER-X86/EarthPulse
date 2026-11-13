import h5py
import os

files = {
    "Cycle 028": "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5",
    "Cycle 032": "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5",
    "Cycle 033": "Nisar.h5"
}

for name, path in files.items():
    print(f"=== {name} ({path}) ===")
    if not os.path.exists(path):
        print("  FILE NOT FOUND")
        continue
    with h5py.File(path, 'r') as f:
        # Check identification or metadata groups
        # NISAR HDF5 structure typically has /identification or similar
        print("  Keys:", list(f.keys()))
        if 'identification' in f:
            ident = f['identification']
            print("  Identification keys:", list(ident.keys()))
            for k in ident.keys():
                try:
                    val = ident[k][()]
                    print(f"    {k}: {val}")
                except Exception as e:
                    print(f"    {k}: <group or unreadable>")
