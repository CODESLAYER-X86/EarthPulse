import h5py
import numpy as np

# Load a sample granule to inspect coordinate arrays
# Using Nisar.h5 which is the Cycle 033 reference granule
file_path = 'Nisar.h5'

try:
    with h5py.File(file_path, 'r') as f:
        # Assuming typical GCOV structure, check for coordinate datasets
        # These are usually found in the grid or metadata sections
        # Based on previous work, look for something like /data/xCoordinates or similar
        
        # List all keys to find where coordinates are
        def print_structure(name, obj):
            if isinstance(obj, h5py.Dataset):
                if 'xCoordinates' in name or 'yCoordinates' in name:
                    print(f"Dataset: {name}, Shape: {obj.shape}, Dtype: {obj.dtype}")
        
        f.visititems(print_structure)
        
except Exception as e:
    print(f"Error inspecting file: {e}")
