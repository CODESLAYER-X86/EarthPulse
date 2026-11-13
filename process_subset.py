import h5py
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import from_origin

# 1. Read a subset of Frequency A (e.g., 1024x1024 window from the center or top-left)
# Let's find an area with valid data (mask != 255)
with h5py.File("Nisar.h5", "r") as f:
    base = "/science/LSAR/GCOV/grids/frequencyA"
    
    # Let's find a region where mask has valid pixels (not 255)
    mask_ds = f[f"{base}/mask"]
    # Scan through chunks or rows to find non-255 pixels
    # Or just grab a region we know has data. Let's look at a 1024x1024 window starting around row 10000, col 10000
    row_start, col_start = 10000, 10000
    window_size = 1024
    
    hhhh = f[f"{base}/HHHH"][row_start:row_start+window_size, col_start:col_start+window_size]
    hvhv = f[f"{base}/HVHV"][row_start:row_start+window_size, col_start:col_start+window_size]
    mask = mask_ds[row_start:row_start+window_size, col_start:col_start+window_size]
    
    x_coords = f[f"{base}/xCoordinates"][col_start:col_start+window_size]
    y_coords = f[f"{base}/yCoordinates"][row_start:row_start+window_size]
    
    # Get projection WKT
    proj_group = f[f"{base}/projection"]
    spatial_ref = proj_group.attrs['spatial_ref'].decode('utf-8')
    
    # Get spacing
    x_spacing = f[f"{base}/xCoordinateSpacing"][()]
    y_spacing = f[f"{base}/yCoordinateSpacing"][()]

print(f"Subset shape: {hhhh.shape}")
print(f"HHHH valid pixels in subset: {np.sum(~np.isnan(hhhh))}")

# Convert to decibels for visualization if appropriate (10 * log10(x), handling zeros/nans)
# Note: NISAR GCOV is power (gamma0 or sigma0). dB = 10 * log10(val)
with np.errstate(divide='ignore', invalid='ignore'):
    hhhh_db = 10.0 * np.log10(hhhh)
    hvhv_db = 10.0 * np.log10(hvhv)

# Plotting preview
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

im0 = axes[0].imshow(hhhh_db, cmap='gray', vmin=-30, vmax=0)
axes[0].set_title('HHHH (dB)')
fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

im1 = axes[1].imshow(hvhv_db, cmap='gray', vmin=-35, vmax=-5)
axes[1].set_title('HVHV (dB)')
fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

im2 = axes[2].imshow(mask, cmap='viridis')
axes[2].set_title('Mask')
fig.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)

plt.tight_layout()
plt.savefig('frequencyA_preview.png', dpi=300)
plt.close()
print("Saved frequencyA_preview.png")

# Export to GeoTIFF
# Rasterio transform from top-left coordinates
# xCoordinates and yCoordinates are center coordinates. Top-left of pixel (0,0) is x[0] - x_spacing/2, y[0] + y_spacing/2
transform = from_origin(x_coords[0] - x_spacing/2.0, y_coords[0] + y_spacing/2.0, x_spacing, y_spacing)

# Stack bands: HHHH, HVHV, mask
export_data = np.stack([
    np.nan_to_num(hhhh, nan=-9999.0),
    np.nan_to_num(hvhv, nan=-9999.0),
    mask.astype(np.float32)
])

with rasterio.open(
    'frequencyA_subset.tif',
    'w',
    driver='GTiff',
    height=window_size,
    width=window_size,
    count=3,
    dtype=rasterio.float32,
    crs=spatial_ref,
    transform=transform,
    nodata=-9999.0
) as dst:
    dst.write(export_data)
    dst.set_band_description(1, 'HHHH (linear power)')
    dst.set_band_description(2, 'HVHV (linear power)')
    dst.set_band_description(3, 'Mask')

print("Saved frequencyA_subset.tif successfully!")
