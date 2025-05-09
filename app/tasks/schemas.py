from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.tasks.enums import StatusEnum


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.PENDING
    priority: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[StatusEnum]
    priority: Optional[int]


class TaskPartialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_by_name=True,
    )


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(
        from_attributes=True,
    )
