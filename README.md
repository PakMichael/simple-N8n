# simple-N8n
## Simple workflow engine POC

The origina task stated:
> Create a flow manager system where tasks are executed sequentially. The flow must include
conditions to evaluate the results of each task and determine whether to proceed to the next
task or end the flow.

And provided the [original JSON fixture](default_flow_fixture.json)

## Solution

Given the time restrictions some of the code was forgone. The project doesn't provide:
- tests
- logging
- task completion state management

The project does provide:
- Task types. They weren't in the task description, but needed to be implemented. (Only available when building state step-by-step. Loading from `.json` will set `type='fetch'` for all tasks) 
- Endoint to build the state from [original JSON fixture](default_flow_fixture.json) at `/build-flow/`
- Endpoints to build the state step by step, by creating `Flow`, attaching `Tasks`, and providing `Conditions`.
- Endpoint to run the `Flow` at `/flow-start/`
- Default endpoint `/docs/` to get OpenAPI representation of all available endpoints 


## What to expect

Once you built a state, you can run `/flow-start/` with `Flow.uuid`. 
Pay attention to the terminal window. Because there's no task completion state management the only way to track task execution is by following the `print()` statements, e.g.

```
Running fetch() for task_uuid=b4382108-1cb4-4aaf-8d46-504892c9a028
Flow completed: no conditions found
```

## How to run

First clone and run the database instance from this repo https://github.com/PakMichael/simple-postgres-environment 

Then run the current project by calling
```
docker-compose --env-file .env.dev up 
```
Here's the `.env.dev` itself:
```
DB_NAME=default_database
DB_USER=dev
DB_PASSWORD=password
DB_HOST=host.docker.internal
DB_PORT=5432
```
Don't forget to run migrations by calling the following command from within docker container

```
alembic upgrade head
```

You should be all set now.

