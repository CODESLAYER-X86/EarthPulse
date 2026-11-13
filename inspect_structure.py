import h5py

file_path = "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"

with h5py.File(file_path, 'r') as f:
    # Need to find where the data is. Based on previous outputs, likely:
    # science/LSAR/GCOV/grids/frequencyA/HH
    # Let's inspect the file structure first.
    def print_structure(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"{name}: shape={obj.shape}")
    
    f.visititems(print_structure)
