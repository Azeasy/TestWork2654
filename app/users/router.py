from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.users.schemas import UserCreate, UserLogin, UserRead, Token
from app.users.service import UserService
from app.core.security import create_access_token, create_refresh_token,\
    oauth2_scheme, credentials_exception, HTTPAuthorizationCredentials
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        new_user = await service.register(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_user


@router.post("/login", response_model=Token)
async def login(data: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    user = await service.authenticate(data.email, data.password)  # Make sure authenticate is async in UserService
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(sub=str(user.id))
    refresh_token = create_refresh_token(sub=str(user.id))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
async def refresh(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    from jose import JWTError, jwt
    from app.core.config import settings

    try:
        token = credentials.credentials
        if not token:
            raise credentials_exception
        token = token.split(" ")[1] if " " in token else token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    access_token = create_access_token(sub=user_id)
    return {"access_token": access_token, "refresh_token": token, "token_type": "bearer"}
