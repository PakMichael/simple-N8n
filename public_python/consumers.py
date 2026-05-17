import asyncio
import json
import uuid

from sqlalchemy import select

from public_python.constants import MAIN_LOOP_CHANNEL
from public_python.db_config import SessionLocal
from public_python.redis_conf import async_redis_client
from public_python.task.models import Task
from public_python.workflow.models import Condition


async def fetch(task: Task):
    print(f"Running fetch() for task_uuid={task.uuid}")
    await asyncio.sleep(1)


async def process(task: Task):
    print(f"Running process() for task_uuid={task.uuid}")
    await asyncio.sleep(1)


async def store(task: Task):
    print(f"Running store() for task_uuid={task.uuid}")
    await asyncio.sleep(1)


async def fallback_task(task: Task):
    print(f"Failed to find an executor for task_uuid={task.uuid}")


allowed_tasks = {"fetch": fetch, "process": process, "store": store}


async def process_task(task_uuid: uuid.UUID):
    async with SessionLocal() as session:
        db_task = await session.get(Task, task_uuid)

        executor = allowed_tasks.get(db_task.type, fallback_task)

        task_status = "success"

        try:
            await executor(task=db_task)
        except:
            print(f"Task {db_task} failed")  # this will be a logger.exception()
            task_status = "failed"

        stmt = select(Condition).where(Condition.source_task_uuid == task_uuid)

        result = await session.execute(stmt)

        db_condition = result.scalars().first()

        if not db_condition:
            print("Flow completed: no conditions found")
            return

        next_task_uuid = db_condition.target_task_success

        if task_status == 'failed':
            next_task_uuid = db_condition.target_task_failure

        if not next_task_uuid:
            print("Flow completed: No 'target_task_failure' provided")
            return

        await async_redis_client.publish(
            MAIN_LOOP_CHANNEL,
            json.dumps(
                {
                    "type": "run_task",
                    "task_uuid": str(next_task_uuid),
                }
            ),
        )


async def main_loop_consumer():
    pubsub = async_redis_client.pubsub()
    await pubsub.subscribe(MAIN_LOOP_CHANNEL)

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        data = json.loads(message["data"])

        if "type" not in data:
            continue

        if data["type"] == "run_task":
            task_uuid = data["task_uuid"]
            await asyncio.create_task(process_task(task_uuid))
