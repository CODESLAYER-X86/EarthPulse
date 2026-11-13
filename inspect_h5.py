import h5py

file_path = "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"
with h5py.File(file_path, 'r') as f:
    def print_name(name):
        if 'science/LSAR/GCOV/grids/frequencyA' in name:
            print(name)
    f.visit(print_name)
