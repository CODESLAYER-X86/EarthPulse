import h5py
import numpy as np
import rasterio
from rasterio.transform import from_origin
import os
import json

# AOI
ROW_SLICE = slice(1490, 1990)
COL_SLICE = slice(13524, 14024)
SHAPE = (500, 500)

# Input files
cycles = {
    'cycle_028': 'data/NISAR_L2_PR_GCOV_028_139_D_092_4005_DHDH_A_20260822T203740_20260822T203818_P05023_N_F_J_001.h5',
    'cycle_032': 'data/NISAR_L2_PR_GCOV_032_139_D_092_4005_DHDH_A_20261009T203740_20261009T203818_P05023_N_F_J_001.h5',
    'cycle_033': 'Nisar.h5'
}

def read_h5_data(file_path):
    with h5py.File(file_path, 'r') as f:
        # Accessing datasets
        hh = f['science/LSAR/GCOV/grids/frequencyA/HHHH'][ROW_SLICE, COL_SLICE]
        hv = f['science/LSAR/GCOV/grids/frequencyA/HVHV'][ROW_SLICE, COL_SLICE]
        mask = f['science/LSAR/GCOV/grids/frequencyA/mask'][ROW_SLICE, COL_SLICE]
        # Get coordinates for transform
        y_coords = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][ROW_SLICE]
        x_coords = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][COL_SLICE]
    
    # Calculate transform (assuming EPSG:32725)
    pixel_size = 10.0
    transform = from_origin(x_coords[0] - pixel_size/2, y_coords[0] + pixel_size/2, pixel_size, pixel_size)
    
    return hh, hv, mask, transform

def process_cycle(cycle_name, file_path):
    os.makedirs(f'data/processed/{cycle_name}', exist_ok=True)
    hh, hv, mask, transform = read_h5_data(file_path)
    
    # Validity
    valid = (mask >= 1) & (mask <= 254) & np.isfinite(hh) & (hh > 0) & np.isfinite(hv) & (hv > 0)
    
    # Conversions
    hh_db = np.where(valid, 10 * np.log10(hh), -9999.0).astype(np.float32)
    hv_db = np.where(valid, 10 * np.log10(hv), -9999.0).astype(np.float32)
    valid_mask = valid.astype(np.uint8)
    
    # Export
    meta = {
        'driver': 'GTiff',
        'height': SHAPE[0],
        'width': SHAPE[1],
        'count': 1,
        'dtype': 'float32',
        'crs': 'EPSG:32725',
        'transform': transform,
        'nodata': -9999.0
    }
    
    def write_tif(filename, data, dtype='float32', nodata=-9999.0):
        m = meta.copy()
        m.update({'dtype': dtype, 'nodata': nodata})
        with rasterio.open(f'data/processed/{cycle_name}/{filename}', 'w', **m) as dst:
            dst.write(data.astype(dtype), 1)

    write_tif('HH_linear.tif', hh)
    write_tif('HV_linear.tif', hv)
    write_tif('HH_db.tif', hh_db)
    write_tif('HV_db.tif', hv_db)
    write_tif('validity_mask.tif', valid_mask, dtype='uint8', nodata=0)
    
    return valid, hh_db, hv_db

# Process all
results = {}
os.makedirs('data/temporal', exist_ok=True)
os.makedirs('data/ml', exist_ok=True)

valid_masks = []
for cycle_name, file_path in cycles.items():
    v, h, hv = process_cycle(cycle_name, file_path)
    results[cycle_name] = {'valid': v, 'hh': h, 'hv': hv}
    valid_masks.append(v)

# Common valid mask
common_valid = np.logical_and.reduce(valid_masks).astype(np.uint8)
# Export common valid mask (reuse meta for uint8)
meta = {
    'driver': 'GTiff',
    'height': SHAPE[0],
    'width': SHAPE[1],
    'count': 1,
    'dtype': 'uint8',
    'crs': 'EPSG:32725',
    'transform': rasterio.open(f'data/processed/cycle_028/validity_mask.tif').transform,
    'nodata': 0
}
with rasterio.open('data/temporal/common_valid_mask.tif', 'w', **meta) as dst:
    dst.write(common_valid, 1)

# Temporal diffs
diffs = {}
combinations = [('028', '032'), ('032', '033'), ('028', '033')]
for c1, c2 in combinations:
    # HH
    hh_diff = results[f'cycle_{c2}']['hh'] - results[f'cycle_{c1}']['hh']
    # HV
    hv_diff = results[f'cycle_{c2}']['hv'] - results[f'cycle_{c1}']['hv']
    
    diffs[f'HH_diff_{c1}_{c2}'] = hh_diff
    diffs[f'HV_diff_{c1}_{c2}'] = hv_diff
    
    # Export
    meta['dtype'] = 'float32'
    meta['nodata'] = -9999.0
    with rasterio.open(f'data/temporal/HH_diff_{c1}_{c2}.tif', 'w', **meta) as dst:
        dst.write(hh_diff, 1)
    with rasterio.open(f'data/temporal/HV_diff_{c1}_{c2}.tif', 'w', **meta) as dst:
        dst.write(hv_diff, 1)

# ML stack
features = [
    results['cycle_028']['hh'], results['cycle_032']['hh'], results['cycle_033']['hh'],
    results['cycle_028']['hv'], results['cycle_032']['hv'], results['cycle_033']['hv'],
    diffs['HH_diff_028_032'], diffs['HH_diff_032_033'], diffs['HH_diff_028_033'],
    diffs['HV_diff_028_032'], diffs['HV_diff_032_033'], diffs['HV_diff_028_033']
]

feature_stack = np.stack(features)
meta['count'] = 12
with rasterio.open('data/ml/feature_stack.tif', 'w', **meta) as dst:
    dst.write(feature_stack)

# Metadata
feature_names = [
    'hh_028_db', 'hh_032_db', 'hh_033_db',
    'hv_028_db', 'hv_032_db', 'hv_033_db',
    'hh_diff_028_032', 'hh_diff_032_033', 'hh_diff_028_033',
    'hv_diff_028_032', 'hv_diff_032_033', 'hv_diff_028_033'
]
metadata = {
    'dimensions': SHAPE,
    'crs': 'EPSG:32725',
    'transform': list(meta['transform']),
    'nodata': -9999.0,
    'feature_names': feature_names,
    'statistics': {
        name: {
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
            'mean': float(np.mean(arr)),
            'std': float(np.std(arr))
        } for name, arr in zip(feature_names, features)
    }
}
with open('data/ml/feature_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

# Project manifest
all_files = []
for root, dirs, files in os.walk('data'):
    for file in files:
        if file.endswith('.tif') or file.endswith('.json'):
            path = os.path.join(root, file)
            all_files.append({
                'path': path,
                'shape': SHAPE if file.endswith('.tif') else None,
                'status': 'SUCCESS'
            })

manifest = {
    'files': all_files
}
with open('data/project_manifest.json', 'w') as f:
    json.dump(manifest, f, indent=4)
