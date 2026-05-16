import uuid as _uuid

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from public_python.db_config import Base


class FlowTask(Base):
    __tablename__ = "flow_task"

    uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=_uuid.uuid4
    )

    is_start_task: Mapped[bool] = mapped_column(Boolean)

    flow_uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("flow.uuid", ondelete="CASCADE"),
    )
    task_uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("task.uuid", ondelete="CASCADE"),
        unique=True,
    )
