from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.models.review import Review


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def count_all(self) -> int:
        stmt = select(func.count(Product.id))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def list_paginated(self, skip: int, limit: int) -> list[dict]:
        stmt = (
            select(
                Product.id,
                Product.title,
                Product.description,
                Product.image_url,
                func.avg(Review.rating).label("average_rating"),
                func.count(Review.id).label("review_count"),
            )
            .outerjoin(Review, Product.id == Review.product_id)
            .group_by(Product.id)
            .order_by(Product.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        return [
            {
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "image_url": row.image_url,
                "average_rating": round(float(row.average_rating), 1) if row.average_rating else None,
                "review_count": row.review_count,
            }
            for row in rows
        ]

    async def get_by_id_with_reviews(self, product_id: int) -> dict | None:
        stmt = (
            select(Product)
            .options(selectinload(Product.reviews).selectinload(Review.user))
            .where(Product.id == product_id)
        )
        result = await self.db.execute(stmt)
        product = result.scalar_one_or_none()
        if not product:
            return None

        reviews = product.reviews
        avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else None

        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "image_url": product.image_url,
            "average_rating": avg_rating,
            "review_count": len(reviews),
            "reviews": [
                {
                    "id": r.id,
                    "product_id": r.product_id,
                    "user_id": r.user_id,
                    "user": r.user.name,
                    "rating": r.rating,
                    "comment": r.comment,
                    "created_at": r.created_at,
                }
                for r in reviews
            ],
        }

    async def create(self, title: str, description: str, image_url: str | None) -> Product:
        product = Product(title=title, description=description, image_url=image_url)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product