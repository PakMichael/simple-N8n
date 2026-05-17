import enum
import uuid as _uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from public_python.db_config import Base


class TaskType(str, enum.Enum):
    fetch = "fetch"
    process = "process"
    store = "store"


class Task(Base):
    __tablename__ = "task"

    uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=_uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
