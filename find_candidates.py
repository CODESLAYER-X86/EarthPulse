import h5py
import numpy as np
from pyproj import Transformer

h5_path = 'Nisar.h5'

def find_candidate_indices():
    with h5py.File(h5_path, 'r') as f:
        x_path = '/science/LSAR/GCOV/grids/frequencyB/xCoordinates'
        y_path = '/science/LSAR/GCOV/grids/frequencyB/yCoordinates'
        
        x = f[x_path][:]
        y = f[y_path][:]
        
        # 1. Potengi Estuary (Rio Grande do Norte): ~ 5.81°S, 35.25°W -> Wait, let's check UTM 25S coords for Natal/Potengi
        # Natal is around Lat -5.79, Lon -35.20
        # Let's transform Lat/Lon to EPSG:32725
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:32725", always_xy=True)
        
        candidates = [
            ("Potengi Estuary (Natal, RN)", -35.2100, -5.7900),
            ("Mamanguape River Estuary (Paraíba)", -35.1200, -6.8200),
            ("Rio Trairi / Baía Formosa (RN)", -35.0000, -6.3500)
        ]
        
        print("Candidate coordinates search in grid (EPSG:32725):")
        for name, lon, lat in candidates:
            easting, northing = transformer.transform(lon, lat)
            # Find nearest row and col
            col_idx = np.argmin(np.abs(x - easting))
            row_idx = np.argmin(np.abs(y - northing))
            print(f"\n--- {name} ---")
            print(f"Target Lon/Lat: {lon}, {lat}")
            print(f"Target Easting/Northing: {easting:.2f}, {northing:.2f}")
            print(f"Nearest Grid Index: Row {row_idx}, Col {col_idx}")
            print(f"Grid Coordinate at Index: X={x[col_idx]}, Y={y[row_idx]}")
            
            # Suggest a 5000x5000 window centered or starting here
            row_start = max(0, row_idx - 2500)
            row_end = row_start + 5000
            col_start = max(0, col_idx - 2500)
            col_end = col_start + 5000
            print(f"Proposed 5000x5000 Window: Rows {row_start}–{row_end}, Cols {col_start}–{col_end}")
            
            # Center of this window in EPSG:32725 and EPSG:4326
            center_x = (x[col_start] + x[col_end-1]) / 2
            center_y = (y[row_start] + y[row_end-1]) / 2
            c_lon, c_lat = Transformer.from_crs("EPSG:32725", "EPSG:4326", always_xy=True).transform(center_x, center_y)
            print(f"Window Center: Easting {center_x}, Northing {center_y} -> Lat {c_lat:.4f}, Lon {c_lon:.4f}")

if __name__ == "__main__":
    find_candidate_indices()
