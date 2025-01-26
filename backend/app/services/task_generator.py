from typing import List
import json

import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import child as child_crud
from app.schemas.task import TaskTemplateCreate
from app.schemas.user import UserResponse
from app.schemas.task_generator import (
    TaskGenerationPayload,
    TaskGenerationRequest,
    TaskGenerationResponse,
    ChildDescription
)

import app.crud.task as task_crud

class TaskGenerationService:
    def __init__(self, db: Session):
        self.db = db
        self.endpoint = "http://openai:8010/generate_tasks"

    async def generate_templates(
        self,
        request: TaskGenerationRequest,
        parent: UserResponse
    ) -> str:
        # Получаем данные о ребенке
        child = child_crud.get_child(self.db, request.child_id, parent.id)
        if not child:
            raise HTTPException(status_code=404, detail="Ребенок не найден")

        # Формируем запрос для LLM
        payload = TaskGenerationPayload(
            child_description=ChildDescription(
                age=child.age,
                gender=child.gender,
                interests=child.interests,
            ),
            tasks_description={
                "creative_tasks": {
                    "amount": request.task_count,
                    "topics": [request.description] if request.description else []
                }
            }
        )

        try:
            response = requests.get(self.endpoint, json=payload.model_dump())
            response.raise_for_status()

            result = response.json()
            if result.get('error'):
                raise HTTPException(status_code=500, detail=result['error'])

            tasks_data = json.loads(result['tasks'])
            new_tasks = [
                TaskTemplateCreate(
                    child_id=child.id,
                    title=task['title'],
                    description=task['text'],
                    points_value=10,
                    schedule_type='once'
                )
                for task in tasks_data['tasks']
            ]

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при обращении к сервису генерации: {str(e)}"
            )

        for task in new_tasks:
            task_crud.create_task_template(self.db, task)

        return "Задания успешно сгенерированы"