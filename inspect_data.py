import h5py
import numpy as np

def inspect_group(f, group_path):
    print(f"--- Group: {group_path} ---")
    if group_path not in f:
        print(f"Group {group_path} not found.")
        return

    group = f[group_path]
    for name in group:
        item = group[name]
        if isinstance(item, h5py.Dataset):
            print(f"\nDataset: {name}")
            print(f"  Shape: {item.shape}")
            print(f"  Dtype: {item.dtype}")
            print(f"  Attributes:")
            for attr_name, attr_value in item.attrs.items():
                # Clean up display of potentially large arrays
                if isinstance(attr_value, np.ndarray) and attr_value.size > 5:
                    print(f"    {attr_name}: [array of size {attr_value.size}]")
                else:
                    print(f"    {attr_name}: {attr_value}")
            
            # Read a small subset for statistics (100x100)
            if len(item.shape) >= 1:
                # Handle cases where shape is (2,) or string datasets
                if item.dtype.kind in ['S', 'U']:
                    print(f"  (Skipping stats for string dataset)")
                    continue
                
                subset_shape = tuple(min(dim, 100) for dim in item.shape)
                # Correct indexing for multi-dimensional arrays
                slices = tuple(slice(0, dim) for dim in subset_shape)
                subset = item[slices]
                
                if subset.size > 0:
                    valid_data = subset[~np.isnan(subset)] if np.issubdtype(subset.dtype, np.floating) else subset
                    if valid_data.size > 0:
                        print(f"  Stats (subset {subset_shape}):")
                        print(f"    Min: {np.min(valid_data)}")
                        print(f"    Max: {np.max(valid_data)}")
                        print(f"    Mean: {np.mean(valid_data)}")
        elif isinstance(item, h5py.Group):
            print(f"\nSubgroup: {name}")

with h5py.File("Nisar.h5", "r") as f:
    inspect_group(f, "/science/LSAR/GCOV/grids/frequencyA")
    inspect_group(f, "/science/LSAR/GCOV/grids/frequencyB")
