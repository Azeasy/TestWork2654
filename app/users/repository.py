from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.models import User
from app.users.schemas import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).filter(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user: UserCreate) -> User:
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
