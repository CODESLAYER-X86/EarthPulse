import h5py
import numpy as np
from pyproj import Transformer

# Mangrove sites in decimal degrees
mangrove_sites = [
    (-5.763056, -35.236111), # ~5°45′47″S, 35°14′10″W
    (-5.758611, -35.199722)  # ~5°45′31″S, 35°11′59″W
]

# Coordinate transformation: WGS84 (EPSG:4326) to UTM Zone 25S (EPSG:32725)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32725", always_xy=True)

# Path to the GCOV file
file_path = "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"

with h5py.File(file_path, 'r') as f:
    x_coords = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    y_coords = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]

for i, (lat, lon) in enumerate(mangrove_sites):
    easting, northing = transformer.transform(lon, lat)
    
    # Find nearest index
    col_idx = (np.abs(x_coords - easting)).argmin()
    row_idx = (np.abs(y_coords - northing)).argmin()
    
    print(f"Mangrove Site {i+1}: Lat={lat}, Lon={lon}")
    print(f"  UTM (EPSG:32725): Easting={easting:.2f}, Northing={northing:.2f}")
    print(f"  Raster Indices: Row={row_idx}, Col={col_idx}")
    print(f"  Raster Coords: X={x_coords[col_idx]:.2f}, Y={y_coords[row_idx]:.2f}")
    print("-" * 30)
