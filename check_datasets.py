import h5py

paths = [
    ("Cycle 028", "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5"),
    ("Cycle 032", "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"),
    ("Cycle 033", "Nisar.h5")
]

for name, fp in paths:
    print(f"=== {name} ===")
    with h5py.File(fp, 'r') as f:
        freq_a = f['science/LSAR/GCOV/grids/frequencyA']
        print("Datasets in frequencyA:", list(freq_a.keys()))
        if 'HH' in freq_a:
            print("HH shape:", freq_a['HH'].shape, "dtype:", freq_a['HH'].dtype)
        if 'HV' in freq_a:
            print("HV shape:", freq_a['HV'].shape, "dtype:", freq_a['HV'].dtype)
        if 'xCoordinates' in freq_a:
            print("xCoordinates shape:", freq_a['xCoordinates'].shape)
        if 'yCoordinates' in freq_a:
            print("yCoordinates shape:", freq_a['yCoordinates'].shape)
