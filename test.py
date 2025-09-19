from sentinelhub import (
    SHConfig,
    CRS,
    Geometry,
    MimeType,
    SentinelHubRequest,
    DataCollection,
)
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# API Keys
config = SHConfig()
config.instance_id = "c23f9095-0974-406c-9d58-2b53346bc6ff"
config.sh_client_id = "09c0e84a-114e-45c4-9b31-5d8aee8ce1bd"
config.sh_client_secret = "aBFUCIS9NtDez8JvpLnbyS1m1ngtyDCA"

# Coords of your farm
polygon_coords = [
    [
        [30.248299, 57.115204],
        [30.249372, 57.11354],
        [30.247272, 57.110829],
        [30.245464, 57.112530],
        [30.248299, 57.115204]
    ]
]
geometry = Geometry(Polygon(polygon_coords[0]), crs=CRS.WGS84)


# NDRE Scripts
evalscript_ndre = """
//VERSION=3
function setup() {
  return { input: ["B05","B08"], output: { bands: 1, sampleType: "FLOAT32" } };
}
function evaluatePixel(sample) {
  return [(sample.B08 - sample.B05) / (sample.B08 + sample.B05)];
}
"""

# sentinel request
request = SentinelHubRequest(
    evalscript=evalscript_ndre,
    input_data=[SentinelHubRequest.input_data(DataCollection.SENTINEL2_L2A)],
    responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
    geometry=geometry,
    size=(512, 512),
    config=config,
)

# get data
ndre_data = request.get_data()[0]
print("NDRE shape:", ndre_data.shape)

# save geoTIFF
out_file = "ndre_polygon.tif"
with rasterio.open(
    out_file,
    "w",
    driver="GTiff",
    height=ndre_data.shape[0],
    width=ndre_data.shape[1],
    count=1,
    dtype="float32",
    crs="EPSG:4326",
    transform=rasterio.transform.from_bounds(
        *geometry.geometry.bounds, ndre_data.shape[1], ndre_data.shape[0]
    ),
) as dst:
    dst.write(ndre_data.astype(np.float32), 1)

print(f"GeoTIFF saved as {out_file}")

# Show NDRE plot
plt.imshow(ndre_data, cmap="RdYlGn")
plt.colorbar(label="NDRE")
plt.title("NDRE (Sentinel-2, 10m resolution)")
plt.show()
