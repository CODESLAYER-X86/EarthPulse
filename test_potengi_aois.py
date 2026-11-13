import h5py
import numpy as np
from pyproj import Transformer

# Mangrove sites and estuary center
# Site 1: 5°45′47″S, 35°14′10″W -> -5.763056, -35.236111
# Site 2: 5°45′31″S, 35°11′59″W -> -5.758611, -35.199722
# Estuary center roughly midway or around Site 2 / Natal center
estuary_center_lat = -5.76
estuary_center_lon = -35.21

transformer = Transformer.from_crs("EPSG:4326", "EPSG:32725", always_xy=True)
inv_transformer = Transformer.from_crs("EPSG:32725", "EPSG:4326", always_xy=True)

center_easting, center_northing = transformer.transform(estuary_center_lon, estuary_center_lat)

file_path = "data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5"

with h5py.File(file_path, 'r') as f:
    x_coords = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    y_coords = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]
    
    # Check resolution (pixel size)
    dx = x_coords[1] - x_coords[0]
    dy = y_coords[1] - y_coords[0] # usually negative
    print(f"Resolution: dx={dx}, dy={dy}")

    center_col = (np.abs(x_coords - center_easting)).argmin()
    center_row = (np.abs(y_coords - center_northing)).argmin()
    print(f"Estuary Center UTM: E={center_easting:.2f}, N={center_northing:.2f}")
    print(f"Estuary Center Raster: row={center_row}, col={center_col}")
    print(f"Estuary Center Raster Coords: X={x_coords[center_col]}, Y={y_coords[center_row]}")

    # Test candidate windows: 25 km2 (5km x 5km = 500x500 pixels at 10m), 50 km2 (~7.07km x 7.07km = 707x707 pixels), 100 km2 (10km x 10km = 1000x1000 pixels)
    # Let's define by side length in km: 5km, 7.07km, 10km -> or pixel counts: 500x500, 707x707, 1000x1000
    
    candidates = [
        {"name": "25 km² Window (500x500 px)", "size_km": 5.0, "npix": 500},
        {"name": "50 km² Window (~707x707 px)", "size_km": 7.071, "npix": 707},
        {"name": "100 km² Window (1000x1000 px)", "size_km": 10.0, "npix": 1000}
    ]

    for cand in candidates:
        half_pix = cand["npix"] // 2
        r_min = center_row - half_pix
        r_max = center_row + half_pix
        c_min = center_col - half_pix
        c_max = center_col + half_pix
        
        x_min_val = x_coords[c_min]
        x_max_val = x_coords[c_max]
        y_min_val = y_coords[r_max] # note y_coords might be descending
        y_max_val = y_coords[r_min]
        
        lon_min, lat_min = inv_transformer.transform(x_min_val, y_min_val)
        lon_max, lat_max = inv_transformer.transform(x_max_val, y_max_val)
        
        print(f"\n--- {cand['name']} ---")
        print(f"Row slice: {r_min} to {r_max} ({cand['npix']} pixels)")
        print(f"Col slice: {c_min} to {c_max} ({cand['npix']} pixels)")
        print(f"Easting range: {x_min_val:.2f} to {x_max_val:.2f}")
        print(f"Northing range: {y_min_val:.2f} to {y_max_val:.2f}")
        print(f"Geographic bbox: Lat [{lat_min:.4f}, {lat_max:.4f}], Lon [{lon_min:.4f}, {lon_max:.4f}]")
        print(f"Area: {(cand['npix'] * abs(dx) * cand['npix'] * abs(dy)) / 1e6:.2f} km²")
