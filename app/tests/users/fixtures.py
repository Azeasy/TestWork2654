import uuid

import pytest_asyncio
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings
from app.users.models import User


@pytest_asyncio.fixture(scope="session")
async def test_user(db_session):
    user = User(name="John", email="test@example.com", hashed_password="hashedpassword")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="session")
async def test_user_token(test_user):
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(test_user.id)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
