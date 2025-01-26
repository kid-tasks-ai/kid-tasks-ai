from fastapi import FastAPI, Request
from GptWrapper import TasksGenerator


app = FastAPI()

@app.get("/generate_tasks")
async def generate_tasks(request: Request):
    body = await request.body()
    return TasksGenerator.get_tasks(body)