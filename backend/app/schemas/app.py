from pydantic import BaseModel, Field
from datetime import datetime


class LandBaseSchema(BaseModel):
    group_id: int = Field(..., description="group of the land")
    landname: str = Field(..., max_length=250, description=" name of the user's land")

    is_completed: bool = Field(..., description="State of the land")


class LandCreateSchema(LandBaseSchema):
    pass


class LandUpdateSchema(LandBaseSchema):
    pass


class LandResponseSchema(LandBaseSchema):
    id: int = Field(..., description="Unique identifier of the object")

    created_date: datetime = Field(
        ..., description="Creation date and time of the object"
    )
    updated_date: datetime = Field(
        ..., description="Updating date and time of the object"
    )
