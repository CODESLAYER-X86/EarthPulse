import pyproj

# Define UTM Zone 25S (EPSG:32725) and WGS84 (EPSG:4326)
utm = pyproj.CRS('EPSG:32725')
wgs84 = pyproj.CRS('EPSG:4326')

transformer = pyproj.Transformer.from_crs(utm, wgs84, always_xy=True)

# Extents: x: 116,645.0 to 449,995.0; y: 9,055,445.0 to 9,380,155.0
x_min, x_max = 116645.0, 449995.0
y_min, y_max = 9055445.0, 9380155.0

corners = [
    (x_min, y_min),
    (x_max, y_min),
    (x_max, y_max),
    (x_min, y_max)
]

for x, y in corners:
    lon, lat = transformer.transform(x, y)
    print(f"UTM: ({x}, {y}) -> Lat/Lon: ({lat}, {lon})")
