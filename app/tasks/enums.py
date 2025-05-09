from enum import Enum
import sqlalchemy as sa


class StatusEnum(str, Enum):
    PENDING = "pending"
    DONE    = "done"
