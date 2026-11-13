import h5py

def list_keys(name, obj):
    print(name)

with h5py.File('Nisar.h5', 'r') as f:
    print("Metadata keys:")
    f['science/LSAR/GCOV/metadata'].visititems(list_keys)
