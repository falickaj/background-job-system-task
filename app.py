from fastapi import FastAPI, HTTPException, BackgroundTasks
import asyncio
from typing import Optional
from pydantic import BaseModel
import datetime
import re

app = FastAPI()

class Task(BaseModel):
    task_name: str
    schedule_time: Optional[str] = None
    
    @property
    def delay(self) -> Optional[float]:
        if not self.schedule_time:
            return None
        match = re.match(r'^(\d+)d(\d+)h(\d+)m$', self.schedule_time)
        if not match:
            raise ValueError('Invalid schedule_time format')
        days, hours, minutes = map(int, match.groups())
        total_minutes = days * 24 * 60 + hours * 60 + minutes
        return total_minutes * 60  # convert to seconds


async def run_task(task: Task):
    print("Running task:", task.task_name)

@app.post("/schedule-task")
async def schedule_task(task: Task, background_tasks: BackgroundTasks):
    if task.delay is None:
        asyncio.create_task(run_task(task))
        message = "Task queued"
    else:
        delay = task.delay
        if delay <= 0:
            raise HTTPException(status_code=400, detail="Schedule time must be in the future")
        else:
            background_tasks.add_task(asyncio.sleep, delay)
            background_tasks.add_task(run_task, task)
        message = "Task scheduled"
    return {"message": message}

@app.post("/queue-task")
async def queue_task(task: Task):
    asyncio.create_task(run_task(task))
    return {"message": "Task queued"}
