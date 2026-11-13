import h5py
import numpy as np
import json

# Reference granule: Nisar.h5
file_path = 'Nisar.h5'

def get_row_col(x_target, y_target, f):
    x_coords = f['/science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    y_coords = f['/science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]
    
    # Coordinates are in descending Y order (standard for some GIS/SAR datasets)
    # yCoordinates: 9.38016e+06...
    
    # Find nearest index
    col_idx = (np.abs(x_coords - x_target)).argmin()
    row_idx = (np.abs(y_coords - y_target)).argmin()
    
    return row_idx, col_idx

# Proposed Candidates
candidates = {
    "Rio Preguiças": {"x": 300000, "y": 9200000},
    "Delta do Parnaíba": {"x": 200000, "y": 9150000},
    "Eastern Mangroves": {"x": 400000, "y": 9300000}
}

try:
    with h5py.File(file_path, 'r') as f:
        results = {}
        for name, pos in candidates.items():
            r, c = get_row_col(pos['x'], pos['y'], f)
            results[name] = {"row_center": int(r), "col_center": int(c)}
            
        print(json.dumps(results, indent=2))
        
except Exception as e:
    # If h5py fails, we have to rely on h5dump output
    print(f"Error: {e}")
