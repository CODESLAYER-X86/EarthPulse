import h5py
import numpy as np
from pyproj import Transformer

# Path to the HDF5 file
h5_path = 'Nisar.h5'

def inspect_footprint():
    with h5py.File(h5_path, 'r') as f:
        # Based on previous inspection, coordinates are under frequencyB
        # Need to verify the exact path
        # Assuming typical GCOV structure
        x_path = '/science/LSAR/GCOV/grids/frequencyB/xCoordinates'
        y_path = '/science/LSAR/GCOV/grids/frequencyB/yCoordinates'
        
        # Read the arrays
        x = f[x_path][:]
        y = f[y_path][:]
        
        # Get corners
        # x is 1D array of column coordinates (longitude-like in UTM)
        # y is 1D array of row coordinates (latitude-like in UTM)
        # Actually in UTM, x is easting, y is northing
        
        min_x, max_x = np.min(x), np.max(x)
        min_y, max_y = np.min(y), np.max(y)
        
        print(f"Projected Bounds (EPSG:32725):")
        print(f"X: {min_x} - {max_x}")
        print(f"Y: {min_y} - {max_y}")
        
        # Setup transformation from EPSG:32725 to EPSG:4326 (WGS84)
        transformer = Transformer.from_crs("EPSG:32725", "EPSG:4326", always_xy=True)
        
        # Define 4 corners
        corners = [
            (min_x, min_y),
            (max_x, min_y),
            (max_x, max_y),
            (min_x, max_y)
        ]
        
        print("\nGeographic Corners (EPSG:4326):")
        for x_val, y_val in corners:
            lon, lat = transformer.transform(x_val, y_val)
            print(f"Lat: {lat:.4f}, Lon: {lon:.4f}")
            
        # Center
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        center_lon, center_lat = transformer.transform(center_x, center_y)
        print(f"\nCenter (EPSG:4326): Lat: {center_lat:.4f}, Lon: {center_lon:.4f}")

if __name__ == "__main__":
    inspect_footprint()
