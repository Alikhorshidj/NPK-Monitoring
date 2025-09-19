import os
from fastapi import APIRouter, Path, Depends, HTTPException, Query,Request
from fastapi.responses import JSONResponse,FileResponse
from schemas.app import * 
from model.app import LandModel
from model.users import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from auth.jwt_auth import get_authenticated_jwt_user
from utils.ndre import sentinel_ndre
from starlette.concurrency import run_in_threadpool

router = APIRouter(prefix="/app", tags=["App"])

#sample
@router.post("/submit-bbox/{land_id}")
async def submit_bbox(
    request: Request,
    land_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):


    land_obj = db.query(LandModel).filter_by(user_id=user.id, id=land_id).first()
    if not land_obj:
        raise HTTPException(status_code=404, detail="land not found")

    body = await request.json()
    polygon_coords = body.get("polygon_coords")
    start_date = body.get("start_date", "2025-06-01")
    end_date = body.get("end_date", "2025-06-30")

    if not polygon_coords:
        raise HTTPException(status_code=400, detail="polygon_coords is required")

    # وضعیت در حال پردازش
    land_obj.in_process = True
    db.add(land_obj)
    db.commit()
    db.refresh(land_obj)

    # اجرای تابع در threadpool
    res = await run_in_threadpool(
        sentinel_ndre, polygon_coords, land_id, db, start_date, end_date
    )

    return JSONResponse(
        content={
            "status": res,
            "points_received": polygon_coords,
            "date_range": {"start_date": start_date, "end_date": end_date},
            "in_process": land_obj.in_process,
        }
    )




@router.get("/lands/{land_id}/histo")
async def get_ndre_png(
    land_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):

    land_obj = db.query(LandModel).filter_by(user_id=user.id, id=land_id).first()
    if not land_obj:
        raise HTTPException(status_code=404, detail="land not found")


    png_path = f"picture/ndre_png/{land_id}.png"
    if not os.path.exists(png_path):
        raise HTTPException(status_code=404, detail="NDRE PNG not found")

    return FileResponse(
        path=png_path,
        media_type="image/png",
        filename=f"{land_id}.png"
    )


@router.get("/lands", response_model=List[LandResponseSchema])
async def retrieve_lands_list(
    completed: bool = Query(None, description="lands complated or not"),
    group: int = Query(None, description="group of the land"),
    # limit: int=Query(10,gt=0,le=50,description="limit number of items to reterive"), #we have func-bug in here!
    # offset: int=Query(0,gt=0,description="limit number of items to reterive"),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):

    query = db.query(LandModel).filter_by(
        user_id=user.id
    )  # <--- is that a idor bug? all below endopoint have that
    
    #TODO it can better
    if completed is not None :
        query = query.filter_by(is_completed=completed)
    if  group is not None:
        query = query.filter_by(group_id=group)

    return query.all()  # limit(limit).offset(offset)


@router.get("/lands/{land_id}", response_model=LandResponseSchema)
async def retrieve_lands_detail(
    land_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):

    task_obj = db.query(LandModel).filter_by(user_id=user.id, id=land_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="land not found")
    return task_obj


@router.post("/lands", response_model=LandResponseSchema)
async def create_land(
    request: LandCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):
    data = request.model_dump()

    data.update({"user_id": user.id})

    land_obj = LandModel(**data)#bug maybe

    db.add(land_obj)
    db.commit()
    db.refresh(land_obj)
    return land_obj


@router.put("/lands/{land_id}", response_model=LandResponseSchema)
async def update_land(
    request: LandUpdateSchema,
    land_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):

    land_obj = db.query(LandModel).filter_by(user_id=user.id, id=land_id).first()
    if not land_obj:
        raise HTTPException(status_code=404, detail="land not found")

    # Update fields using setattr
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(land_obj, field, value)

    db.commit()  # Commit the changes to the database
    db.refresh(land_obj)  # Refresh the task object to reflect the updated data

    return land_obj  # Return the updated task object


@router.delete("/lands/{land_id}", status_code=204)
async def delete_land(
    land_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_jwt_user),
):
    land_obj = db.query(LandModel).filter_by(user_id=user.id, id=land_id).first()
    if not land_obj:
        raise HTTPException(status_code=404, detail="land not found")
    db.delete(land_obj)
    db.commit()