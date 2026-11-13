import h5py
import numpy as np

base = "/science/LSAR/GCOV/grids/frequencyA"

with h5py.File("Nisar.h5", "r") as f:
    x_coords = f[f"{base}/xCoordinates"]
    y_coords = f[f"{base}/yCoordinates"]
    
    print(f"xCoordinates shape: {x_coords.shape}")
    print(f"yCoordinates shape: {y_coords.shape}")
    
    # Assuming they are 1D arrays
    min_x, max_x = x_coords[0], x_coords[-1]
    min_y, max_y = y_coords[-1], y_coords[0] # Assuming y is decreasing
    
    print(f"X range: {min_x} to {max_x}")
    print(f"Y range: {min_y} to {max_y}")
    
    # EPSG
    proj_group = f[f"{base}/projection"]
    spatial_ref = proj_group.attrs['spatial_ref'].decode('utf-8')
    print(f"Spatial Ref (WKT): {spatial_ref}")
    
    x_spacing = f[f"{base}/xCoordinateSpacing"][()]
    y_spacing = f[f"{base}/yCoordinateSpacing"][()]
    print(f"X Spacing: {x_spacing}")
    print(f"Y Spacing: {y_spacing}")
