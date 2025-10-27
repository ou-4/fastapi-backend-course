from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
tasks = [{'id': 1, 'task': 'Закончить простые бэки', 'status': 'No'}, {'id': 2, 'task': 'Хз', 'status': 'Yes'}]

class CreateTask(BaseModel):
    task: str
    status: str = 'No'
class UpdateTask(BaseModel):
    task: str
    status: str

@app.get("/tasks", tags=['Вывод всех задач'])
def get_tasks():
    return tasks

@app.post("/tasks", tags=['Добавление задачи'])
def create_task(new_task: CreateTask):
    max_id = max(task['id'] for task in tasks)
    tasks.append({'id': max_id + 1, 'task': new_task.task, 'status': new_task.status})
    return {"success": True}

@app.put("/tasks/{task_id}", tags=['Обновление задачи'])
def update_task(task_id: int, update_task: UpdateTask):
    for i in tasks:
        if i['id'] == task_id:
            i['task'] = update_task.task
            i['status'] = update_task.status
            return {"success": True}
     
    raise HTTPException(status_code=404, detail = 'Задача не найдена')

@app.delete("/tasks/{task_id}", tags=['Удаление задачи'])
def delete_task(task_id: int):
    global tasks
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            tasks.pop(i)
            return     {"success": True}     
        
    raise HTTPException(status_code=404, detail = 'Задача не найдена')