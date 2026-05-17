import uuid

from pydantic import BaseModel


class FlowCreate(BaseModel):
    name: str


class CreateFlowTask(BaseModel):
    name: str
    description: str
    is_start_task: bool = False
    flow_uuid: uuid.UUID


class CreateFlowCondition(BaseModel):
    name: str
    description: str
    source_task_uuid: uuid.UUID
    target_task_success_uuid: uuid.UUID
    target_task_failure_uuid: uuid.UUID | None = None
    flow_uuid: uuid.UUID
