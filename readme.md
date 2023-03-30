# Simple background job task from Dev Project

## Run Project
```
pip3 install -r requirements.txt
uvicorn app:app --reload
```
## Test Project

```bash
curl -X POST -H "Content-Type: application/json" -d '{"task_name": "my_task", "schedule_time": "0d0h2m"}' http://localhost:8000/schedule-task
```
    
## Project URL

- [Background Job](https://www.codementor.io/projects/tool/background-job-system-atx32exogo)

