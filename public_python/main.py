import asyncio

from fastapi import FastAPI

from public_python.consumers import main_loop_consumer
from public_python.workflow.routes import workflow_router

app = FastAPI()

app.include_router(workflow_router, prefix="/api")

@app.on_event("startup")
async def start_consumer():
    asyncio.create_task(main_loop_consumer())