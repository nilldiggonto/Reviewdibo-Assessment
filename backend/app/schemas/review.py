from datetime import datetime

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str


class ReviewCreate(ReviewBase):
    product_id: int
    user_id: int


class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


class ReviewOut(ReviewBase):
    id: int
    product_id: int
    user_id: int
    user: str
    created_at: datetime

    model_config = {"from_attributes": True}