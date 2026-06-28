from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.product_repository import ProductRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository
from app.schemas.review import ReviewCreate, ReviewOut, ReviewUpdate
from app.services.review_service import ReviewService

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    return ReviewService(ReviewRepository(db), ProductRepository(db), UserRepository(db))


@router.post("", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def create_review(body: ReviewCreate, service: ReviewService = Depends(get_review_service)):
    return await service.create_review(body.product_id, body.user_id, body.rating, body.comment)


@router.put("/{review_id}", response_model=ReviewOut)
async def update_review(review_id: int, body: ReviewUpdate, service: ReviewService = Depends(get_review_service)):
    return await service.update_review(review_id, body.rating, body.comment)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(review_id: int, service: ReviewService = Depends(get_review_service)):
    await service.delete_review(review_id)