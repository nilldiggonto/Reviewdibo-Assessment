from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, review_id: int) -> Review | None:
        stmt = select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, product_id: int, user_id: int, rating: int, comment: str) -> Review:
        review = Review(product_id=product_id, user_id=user_id, rating=rating, comment=comment)
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        stmt = select(Review).options(selectinload(Review.user)).where(Review.id == review.id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def update(self, review: Review, rating: int | None, comment: str | None) -> Review:
        if rating is not None:
            review.rating = rating
        if comment is not None:
            review.comment = comment
        await self.db.commit()
        await self.db.refresh(review)
        stmt = select(Review).options(selectinload(Review.user)).where(Review.id == review.id)
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def delete(self, review: Review) -> None:
        await self.db.delete(review)
        await self.db.commit()