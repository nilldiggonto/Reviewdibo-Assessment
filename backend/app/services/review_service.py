from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository
from app.schemas.review import ReviewOut


class ReviewService:
    def __init__(
        self,
        review_repo: ReviewRepository,
        product_repo: ProductRepository,
        user_repo: UserRepository,
    ):
        self.review_repo = review_repo
        self.product_repo = product_repo
        self.user_repo = user_repo

    async def create_review(self, product_id: int, user_id: int, rating: int, comment: str) -> ReviewOut:
        product = await self.product_repo.get_by_id_with_reviews(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        review = await self.review_repo.create(product_id, user_id, rating, comment)
        return ReviewOut(
            id=review.id,
            product_id=review.product_id,
            user_id=review.user_id,
            user=review.user.name,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at,
        )

    async def update_review(self, review_id: int, rating: int | None, comment: str | None) -> ReviewOut:
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        updated = await self.review_repo.update(review, rating, comment)
        return ReviewOut(
            id=updated.id,
            product_id=updated.product_id,
            user_id=updated.user_id,
            user=updated.user.name,
            rating=updated.rating,
            comment=updated.comment,
            created_at=updated.created_at,
        )

    async def delete_review(self, review_id: int) -> None:
        review = await self.review_repo.get_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        await self.review_repo.delete(review)