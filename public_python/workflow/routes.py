import json
import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from public_python.constants import MAIN_LOOP_CHANNEL
from public_python.db_config import AsyncSessionDep
from public_python.flow.models import Flow
from public_python.redis_conf import async_redis_client
from public_python.task.models import Task, TaskType
from public_python.workflow.domain.entities import (
    FlowCreate,
    CreateFlowTask,
    CreateFlowCondition,
    FlowBuilder,
)
from public_python.workflow.models import FlowTask, Condition

workflow_router = APIRouter()


@workflow_router.post("/flow/")
async def create_flow(flow: FlowCreate, session: AsyncSessionDep):

    db_flow = Flow(name=flow.name)

    session.add(db_flow)

    await session.commit()
    await session.refresh(db_flow)

    return db_flow


@workflow_router.post("/task/")
async def create_task(task: CreateFlowTask, session: AsyncSessionDep):
    async with session.begin():
        db_task = Task(name=task.name, description=task.description, type=task.type)

        session.add(db_task)
        await session.flush()

        db_flow_task = FlowTask(
            flow_uuid=task.flow_uuid,
            task_uuid=db_task.uuid,
            is_start_task=task.is_start_task,
        )
        session.add(db_flow_task)

    return db_task, db_flow_task


@workflow_router.post("/condition/")
async def create_condition(condition: CreateFlowCondition, session: AsyncSessionDep):
    db_condition = Condition(
        name=condition.name,
        description=condition.description,
        flow_uuid=condition.flow_uuid,
        source_task_uuid=condition.source_task_uuid,
        target_task_success=condition.target_task_success_uuid,
        target_task_failure=condition.target_task_failure_uuid,
    )

    session.add(db_condition)

    await session.commit()
    await session.refresh(db_condition)

    return db_condition


@workflow_router.post("/flow-start/")
async def flow_start(flow_uuid: uuid.UUID, session: AsyncSessionDep):
    stmt = (
        select(Task.uuid)
        .join(FlowTask, FlowTask.flow_uuid == flow_uuid)
        .where(FlowTask.is_start_task == True)
        .where(Task.uuid == FlowTask.task_uuid)
        .limit(1)
    )

    result = await session.execute(stmt)

    task_uuid = result.scalar()

    if not task_uuid:
        raise HTTPException(status_code=400, detail="Flow starting task was not set")

    await async_redis_client.publish(
        MAIN_LOOP_CHANNEL,
        json.dumps(
            {
                "type": "run_task",
                "task_uuid": str(task_uuid),
            }
        ),
    )

    return "Flow started"


@workflow_router.post("/build-flow/")
async def build_flow(raw_flow: FlowBuilder, session: AsyncSessionDep):
    task_uuids = {"end": None}  # Json provides 'end' value as to mean 'do not continue'

    async with session.begin():
        flow = FlowCreate(name=raw_flow.flow.name)

        db_flow = Flow(name=flow.name)

        session.add(db_flow)

        await session.flush()

        for raw_task in raw_flow.flow.tasks:
            db_task = Task(
                name=raw_task.name,
                description=raw_task.description,
                type=TaskType.fetch,
            )

            session.add(db_task)
            await session.flush()

            task_uuids.update({db_task.name: db_task.uuid})

            db_flow_task = FlowTask(
                flow_uuid=db_flow.uuid,
                task_uuid=db_task.uuid,
                is_start_task=raw_task.name == raw_flow.flow.start_task,
            )
            session.add(db_flow_task)

        for raw_condition in raw_flow.flow.conditions:
            db_condition = Condition(
                name=raw_condition.name,
                description=raw_condition.description,
                flow_uuid=db_flow.uuid,
                source_task_uuid=task_uuids[raw_condition.source_task],
                target_task_success=task_uuids[raw_condition.target_task_success],
                target_task_failure=task_uuids[raw_condition.target_task_failure],
            )

            session.add(db_condition)

    return raw_flow
