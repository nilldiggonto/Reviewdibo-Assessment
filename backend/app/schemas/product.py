from typing import Generic, TypeVar

from pydantic import BaseModel

from app.schemas.review import ReviewOut

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProductBase(BaseModel):
    title: str
    description: str
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductListOut(BaseModel):
    id: int
    title: str
    description: str
    image_url: str | None
    average_rating: float | None
    review_count: int

    model_config = {"from_attributes": True}


class ProductDetailOut(BaseModel):
    id: int
    title: str
    description: str
    image_url: str | None
    average_rating: float | None
    review_count: int
    reviews: list[ReviewOut]

    model_config = {"from_attributes": True}
