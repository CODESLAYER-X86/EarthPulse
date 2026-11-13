import h5py
import numpy as np

FILE = "Nisar.h5"

with h5py.File(FILE, "r") as f:
    base = "/science/LSAR/GCOV/grids"

    for freq in ["frequencyA", "frequencyB"]:
        print(f"\n===== {freq} =====")
        group = f[f"{base}/{freq}"]

        for name in ["HHHH", "HVHV", "mask",
                     "xCoordinates", "yCoordinates", "projection"]:

            if name not in group:
                continue

            ds = group[name]

            print(f"\n{name}")
            print("Shape:", ds.shape)
            print("Data type:", ds.dtype)

            if name in ["xCoordinates", "yCoordinates"]:
                values = ds[:]
                print("First:", values[0])
                print("Last:", values[-1])

            elif name == "projection":
                print("Value:", ds[()])

            elif name in ["HHHH", "HVHV"]:
                sample = ds[1000:1010, 1000:1010]
                print("Sample values:\n", sample)
                print("Dataset attributes:", dict(ds.attrs))
