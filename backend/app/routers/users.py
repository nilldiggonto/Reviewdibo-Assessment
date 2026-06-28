from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(body.name, body.email)


@router.get("", response_model=list[UserOut])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.list_users()