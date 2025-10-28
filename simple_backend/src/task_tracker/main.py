from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json

app = FastAPI()

json_name = 'tasks.json'

def load_tasks():
    if not os.path.exists(json_name):
        return []
    
    try:
        with open(json_name, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(task_list):
    with open(json_name, 'w', encoding='utf-8') as file:
        json.dump(task_list, file)

class CreateTask(BaseModel):
    task: str
    status: str = 'No'
    
class UpdateTask(BaseModel):
    task: str
    status: str

@app.get("/tasks", tags=['Вывод всех задач'])
def get_tasks():
    return load_tasks()

@app.post("/tasks", tags=['Добавление задачи'])
def create_task(new_task: CreateTask):
    tasks = load_tasks()
    max_id = max(task['id'] for task in tasks) + 1
    tasks.append({'id': max_id, 'task': new_task.task, 'status': new_task.status})
    save_tasks(tasks)
    return {"success": True}

@app.put("/tasks/{task_id}", tags=['Обновление задачи'])
def update_task(task_id: int, update_task: UpdateTask):
    tasks = load_tasks()
    for i in tasks:
        if i['id'] == task_id:
            i['task'] = update_task.task
            i['status'] = update_task.status
            save_tasks(tasks)
            return {"success": True}
     
    raise HTTPException(status_code=404, detail = 'Задача не найдена')

@app.delete("/tasks/{task_id}", tags=['Удаление задачи'])
def delete_task(task_id: int):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            return     {"success": True}     
        
    raise HTTPException(status_code=404, detail = 'Задача не найдена')