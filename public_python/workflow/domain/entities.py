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


class RawTask(BaseModel):
    name: str
    description: str


class RawCondition(BaseModel):
    name: str
    description: str
    source_task: str
    outcome: str  # ignored in the project - meaning unclear
    target_task_success: str
    target_task_failure: str


class RawFlow(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: list[RawTask]
    conditions: list[RawCondition]


class FlowBuilder(BaseModel):
    flow: RawFlow
