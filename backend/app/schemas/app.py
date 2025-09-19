from pydantic import BaseModel, Field
from datetime import datetime, date


class LandBaseSchema(BaseModel):
    group_id: int = Field(..., description="Group of the land")
    landname: str = Field(..., max_length=250, description="Name of the user's land")


class LandCreateSchema(LandBaseSchema):
    pass


class LandUpdateSchema(LandBaseSchema):
    pass


class LandResponseSchema(LandBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")
    is_completed: bool = Field(..., description="Status of the land")
    acquisition_date: date | None = Field(
        None, description="Acquisition date of the last satellite image"
    )
    created_date: datetime = Field(
        ..., description="Creation date and time of the object"
    )
    updated_date: datetime = Field(
        ..., description="Updating date and time of the object"
    )
