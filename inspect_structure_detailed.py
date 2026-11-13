import h5py

file_paths = [
    "data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5",
    "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5",
    "Nisar.h5"
]

def inspect(file_path):
    print(f"Inspecting: {file_path}")
    with h5py.File(file_path, 'r') as f:
        # Check coords
        freqA = f['science/LSAR/GCOV/grids/frequencyA']
        print(f"  Coordinates in freqA: {'xCoordinates' in freqA} {'yCoordinates' in freqA}")
        
        # Check polarizations
        print(f"  Polarizations in freqA: {list(freqA.keys())}")
        
        # Check HHHH and HVHV
        if 'HHHH' in freqA:
            print(f"  HHHH shape: {freqA['HHHH'].shape}")
        if 'HVHV' in freqA:
            print(f"  HVHV shape: {freqA['HVHV'].shape}")
        else:
             print("  HVHV NOT FOUND")

for fp in file_paths:
    inspect(fp)
