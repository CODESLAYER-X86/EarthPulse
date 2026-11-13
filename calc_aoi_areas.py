import numpy as np
import h5py

# Open one file to get grid dimensions and pixel spacing
with h5py.File('Nisar.h5', 'r') as f:
    xc = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    yc = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]

# Pixel spacing is 10m x 10m = 100 m^2 per pixel = 0.0001 km^2 per pixel

boxes = [
    ("Candidate 1: Rio Preguiças Estuary", slice(10000, 15000), slice(10000, 15000)),
    ("Candidate 2: Delta do Parnaíba Edge", slice(5000, 10000), slice(20000, 25000)),
    ("Candidate 3: Eastern Mangroves", slice(20000, 25000), slice(10000, 15000))
]

for name, y_slice, x_slice in boxes:
    num_pixels = (y_slice.stop - y_slice.start) * (x_slice.stop - x_slice.start)
    area_km2 = num_pixels * 0.0001
    print(f"{name}: {num_pixels} pixels, {area_km2:.2f} km^2")
