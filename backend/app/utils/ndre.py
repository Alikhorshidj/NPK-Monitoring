import os
import numpy as np
from sentinelhub import (
    SHConfig,
    CRS,
    Geometry,
    MimeType,
    SentinelHubRequest,
    DataCollection,
    SentinelHubCatalog
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from core.config import settings
from sqlalchemy.orm import Session
from model.app import LandModel
from datetime import datetime


def sentinel_ndre(polygon_coords, land_id: int, db: Session,
                  start_date="2025-06-01", end_date="2025-06-30"):
    """
    - بررسی وجود تصویر با maxcc < 0.5٪
    - محاسبه NDRE
    - ذخیره در DB
    - اگر تصویر مناسب نبود: status=False
    """

    # API Keys
    config = SHConfig()
    config.instance_id = settings.INSTANCE_ID
    config.sh_client_id = settings.SH_CLIENT_ID
    config.sh_client_secret = settings.SH_CLIENT_SECRET

    # Geometry
    geometry = Geometry(Polygon(polygon_coords), crs=CRS.WGS84)

    # بررسی وجود تصویر مناسب
    catalog = SentinelHubCatalog(config=config)
    results = list(catalog.search(
        DataCollection.SENTINEL2_L2A,
        geometry=geometry,
        time=(start_date, end_date),
        filter="eo:cloud_cover < 0.005",  # ۰.۵٪
        fields={"include": ["id", "properties.datetime"], "exclude": []}
    ))

    if not results:
        # هیچ تصویر مناسبی وجود ندارد
        return {"status": False, "message": "No suitable image found in given date range"}

    # اولین تصویر مناسب
    acquisition_date = results[0]["properties"]["datetime"]
    acquisition_date = datetime.fromisoformat(acquisition_date.replace("Z", "+00:00")).date()

    # NDRE Script
    evalscript_ndre = """
    //VERSION=3
    function setup() {
        return { input: ["B05","B08"], output: { bands: 1, sampleType: "FLOAT32" } };
    }
    function evaluatePixel(sample) {
        return [(sample.B08 - sample.B05) / (sample.B08 + sample.B05)] ;
    }
    """

    # درخواست SentinelHub
    request = SentinelHubRequest(
        evalscript=evalscript_ndre,
        input_data=[SentinelHubRequest.input_data(
            DataCollection.SENTINEL2_L2A,
            time_interval=(start_date, end_date),
            maxcc=0.5
        )],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        geometry=geometry,
        size=(512, 512),
        config=config,
    )

    ndre_data = request.get_data()[0]

    # بررسی اینکه داده واقعی هست یا همه صفر
    if np.all(ndre_data == 0):
        return {"status": False, "message": "NDRE data is empty, no valid pixels"}

    # ذخیره تصویر
    os.makedirs("picture/ndre_png", exist_ok=True)
    png_path = f"picture/ndre_png/{land_id}.png"
    plt.figure(figsize=(6,6))
    plt.imshow(ndre_data, cmap="RdYlGn")
    plt.colorbar(label="NDRE")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close()

    # آپدیت دیتابیس
    land_obj = db.query(LandModel).filter(LandModel.id == land_id).first()
    if land_obj:
        land_obj.is_completed = True
        land_obj.acquisition_date = acquisition_date
        db.add(land_obj)
        db.commit()
        db.refresh(land_obj)

    return {"status": True, "png": png_path, "date": str(acquisition_date)}
