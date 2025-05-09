from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.users.schemas import UserCreate
from app.users.repository import UserRepository
from app.core.security import verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, user: UserCreate):
        existing_user = await self.repo.get_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        return await self.repo.create(user)

    async def authenticate(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
