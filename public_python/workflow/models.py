import uuid as _uuid

from sqlalchemy import ForeignKey, Boolean, UniqueConstraint, String
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

class Condition(Base):
    __tablename__ = "condition_task"

    uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=_uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    flow_uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("flow.uuid", ondelete="CASCADE"),
    )

    source_task_uuid: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("task.uuid", ondelete="CASCADE"),
    )
    target_task_success: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("task.uuid", ondelete="CASCADE"),
    )
    target_task_failure: Mapped[_uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("task.uuid", ondelete="CASCADE"),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint("source_task_uuid", "target_task_success", "target_task_failure"),
    )

