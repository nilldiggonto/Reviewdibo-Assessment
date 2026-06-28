from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.product_repository import ProductRepository
from app.schemas.product import PaginatedResponse, ProductDetailOut, ProductListOut
from app.services.product_service import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


@router.get("", response_model=PaginatedResponse[ProductListOut])
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(9, ge=1, le=100),
    service: ProductService = Depends(get_product_service),
):
    return await service.list_products(page, page_size)


@router.get("/{product_id}", response_model=ProductDetailOut)
async def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    return await service.get_product_detail(product_id)