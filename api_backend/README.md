### API Backend

## TODO

- [ ] split models to web and db models
- [ ] refactor database logic to table classes
- [ ] fix logging (add loguru as main logger and configure it)
- [ ] Add tests

#### Using standard asyncio queue for long running process

````python
import asyncio
from fastapi import FastAPI

app = FastAPI()

fifo_queue = asyncio.Queue()

async def worker():
    while True:
        print(f"Got a job: (size of remaining queue: {fifo_queue.qsize()})")
        job = await fifo_queue.get()
        await job()


@app.on_event("startup")
async def on_start_up():
     # Line of code below is for running asyncio queue worker
     asyncio.create_task(worker())

async def long_running_process():
    print("in a long running task")
    await asyncio.sleep(10)
    print("done with long running task")


@app.post("/process")
async def asyncio_queue():
    """
    Using standard asycio queue for long running process
    """
    print("Queueing a job")
    await fifo_queue.put(long_running_process)
    return {"result": "success"}
    ```
````

#### Using BackgroundTasks for long running process

```python

import time
from fastapi import BackgroundTasks, FastAPI


app = FastAPI()


def process_item(item_id: int):
    # Simulate a long-running process
    time.sleep(5)
    print(f"Processed item {item_id}")

@app.post("/process/{item_id}")
async def process_item_background(item_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_item, item_id)
    return {"message": "Processing started in the background"}
```
