from fastapi import APIRouter,Request
from utils.ndre import sentinel_ndre

router = APIRouter(prefix="/app", tags=["app"])

#sample
@router.post("/submit-bbox")
async def submit_bbox(request: Request):

    polygon_coords = await request.json() 

    res=sentinel_ndre(polygon_coords)
    return {"status": "ok", "points_received": res}