import h5py
import numpy as np
from pyproj import Transformer
import json

h5_path = 'Nisar.h5'
base = "/science/LSAR/GCOV/grids/frequencyA"

with h5py.File(h5_path, 'r') as f:
    x_coords = f[f"{base}/xCoordinates"][:]
    y_coords = f[f"{base}/yCoordinates"][:]
    
    # Check projection
    proj_group = f[f"{base}/projection"]
    # Let's see what attributes are in projection
    proj_wkt = proj_group.attrs.get('spatial_epsg', None)
    print(f"Spatial EPSG from attributes: {proj_wkt}")

min_x, max_x = np.min(x_coords), np.max(x_coords)
min_y, max_y = np.min(y_coords), np.max(y_coords)

print(f"Projected X bounds: {min_x} to {max_x}")
print(f"Projected Y bounds: {min_y} to {max_y}")

# Let's use EPSG:32725 (UTM Zone 25S) as deduced previously, or check if epsg is available.
# Actually, let's look at how epsg is stored or use the previous assumption (UTM 25S is northeastern Brazil).
# Wait, let's verify the EPSG code from the HDF5 file if possible.
