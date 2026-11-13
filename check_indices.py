import h5py
import numpy as np

# Path to the HDF5 file
h5_path = 'Nisar.h5'

def get_grid_indices():
    with h5py.File(h5_path, 'r') as f:
        # Based on previous inspection, grid structure is fixed
        # Need to verify indices that correspond to the footprint
        # Just printing the shape to understand dimensions
        x_path = '/science/LSAR/GCOV/grids/frequencyB/xCoordinates'
        y_path = '/science/LSAR/GCOV/grids/frequencyB/yCoordinates'
        
        x = f[x_path]
        y = f[y_path]
        
        print(f"X Grid shape: {x.shape}")
        print(f"Y Grid shape: {y.shape}")
        
        # Access a small corner to verify index orientation (if needed)
        # Assuming [row, col] or [y, x]
        print(f"Sample X (0,0): {x[0,0]}")
        print(f"Sample X (-1,-1): {x[-1,-1]}")
        print(f"Sample Y (0,0): {y[0,0]}")
        print(f"Sample Y (-1,-1): {y[-1,-1]}")

if __name__ == "__main__":
    get_grid_indices()
