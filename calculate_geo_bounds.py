import h5py
import numpy as np
from pyproj import Transformer

# Path
h5_path = 'Nisar.h5'
base = "/science/LSAR/GCOV/grids/frequencyA"

with h5py.File(h5_path, 'r') as f:
    x_coords = f[f"{base}/xCoordinates"][:]
    y_coords = f[f"{base}/yCoordinates"][:]
    
    min_x, max_x = np.min(x_coords), np.max(x_coords)
    min_y, max_y = np.min(y_coords), np.max(y_coords)
    
    print(f"Projected Bounds (min_x, min_y, max_x, max_y): {min_x}, {min_y}, {max_x}, {max_y}")
    
    # Transformation
    transformer = Transformer.from_crs("EPSG:32725", "EPSG:4326", always_xy=True)
    
    # The bounding box in lat/lon
    # For UTM, transforming the corners is usually sufficient for a rough bounding box.
    corners_x = [min_x, max_x, min_x, max_x]
    corners_y = [min_y, max_y, max_y, min_y]
    
    lons, lats = transformer.transform(corners_x, corners_y)
    
    lat_min, lat_max = np.min(lats), np.max(lats)
    lon_min, lon_max = np.min(lons), np.max(lons)
    
    print(f"Lat/Lon Bounding box (Lat min/max, Lon min/max): {lat_min}, {lat_max}, {lon_min}, {lon_max}")
    
    # Center
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_lon, center_lat = transformer.transform(center_x, center_y)
    print(f"Center: {center_lat}, {center_lon}")
