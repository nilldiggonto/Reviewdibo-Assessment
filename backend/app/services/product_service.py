import math

from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product import PaginatedResponse, ProductDetailOut, ProductListOut


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def list_products(self, page: int, page_size: int) -> PaginatedResponse[ProductListOut]:
        total = await self.repo.count_all()
        skip = (page - 1) * page_size
        rows = await self.repo.list_paginated(skip, page_size)
        items = [ProductListOut(**row) for row in rows]
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if total > 0 else 1,
        )

    async def get_product_detail(self, product_id: int) -> ProductDetailOut:
        data = await self.repo.get_by_id_with_reviews(product_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductDetailOut(**data)