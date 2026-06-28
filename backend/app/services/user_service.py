from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserOut


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, name: str, email: str) -> UserOut:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user = await self.repo.create(name, email)
        return UserOut.model_validate(user)

    async def list_users(self) -> list[UserOut]:
        users = await self.repo.list_all()
        return [UserOut.model_validate(u) for u in users]

    async def get_or_create_user(self, name: str, email: str) -> UserOut:
        user = await self.repo.get_by_email(email)
        if user:
            return UserOut.model_validate(user)
        user = await self.repo.create(name, email)
        return UserOut.model_validate(user)