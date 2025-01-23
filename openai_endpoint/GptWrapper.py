import os
import openai
import tiktoken
import httpx
from pydantic import BaseModel
import requests
from requests.auth import HTTPProxyAuth
from Constants import *
from Exceptions import *
from TaskBank import TasksBank


# Configure your proxy
openai_api_key = os.getenv("OPENAI_API_KEY")
INVENTORY = os.getenv("INVENTORY")

TASKS_FILE = os.getenv("TASKS_FILE")
TASKS_LISTS_NAMES = os.getenv("TASKS_LISTS_NAMES")

task_bank = None
try:
    task_bank = TasksBank(TASKS_FILE, TASKS_LISTS_NAMES)
except TasksDBException as e:
    print("Task DB initialization failed: {e}")


def extract_last_part(text, token_limit=50):
    tokens = text.split()
    return ' '.join(tokens[-token_limit:])


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


class BotMan(BaseModel):
    """A bot that can generate game scenarios for parents and children."""
    @staticmethod
    def get_game(payload):
        try:
            age = payload.get(USER_DATA_AGE)
            inventory = payload.get(USER_DATA_INVENTORY) or INVENTORY
            topic = payload.get(USER_DATA_TOPIC)
            parent_participation_control = payload.get(USER_DATA_PARTICIPATION)
            number_of_children = payload.get(USER_DATA_NUMBER_OF_CHILDREN)
            number_of_actions = payload.get(USER_DATA_NUMBER_OF_ACTIONS)
            user_prompt = f"""
                Ты родитель {number_of_children} детей. Придумай увлекательный сценрий игры для детей.

                Инструкция: Создай сценарий игры, который будет включать в себя интерактивные элементы, соответствующие теме и возрасту детей. 
                Сценарий должен содержать повествовательную составляющую истории и состоять из {number_of_actions} действий. 
                Он должен быть увлекательным, легким для понимания и выполнения детьми указанной возрастной группы, 
                а также включать элементы юмора и творческие задания для активного участия детей. {parent_participation_control}.

                Тема Игры: [{topic}]. Это должна быть приключенческая история, наполненная элементами юмора 
                и фантазии.

                Возрастная Группа: [{age} лет]. Убедитесь, что история и активности подходят для этой возрастной 
                группы.

                Инвентарь: [{inventory}]. Эти предметы должны быть интегрированы в сценарий, чтобы способствовать 
                вовлечению детей в историю и игровые активности.
                """
            
            if task_bank:
                digits = [ int(char) for char in age if char.isdigit() and char in "2345" ]
                age_group = 5
                if digits:
                    age_group = max(digits)
                example = task_bank.get_task_subst(age_group, topic + inventory)
                if example:
                    user_prompt += """

                    Пример сложности и содержания заданий:
                    '''
                        {example}
                    '''
                """
            
            user_prompt += """

                Пример структуры сценария:
                <b>Игровой Сценарий: "Приключения Марио и Друзей"</b>               
                <b>Возрастная Группа:</b> 5-7 лет                
                <b>Инвентарь:</b> Игрушки персонажей из мира Марио, бумага, карандаши, простые предметы для создания препятствий и заданий.

                <b>Введение в Историю:</b>
                "Привет, друзья! Сегодня мы отправимся в удивительное путешествие по миру Марио..."

                <b>1. Строим Уровень из Мира Марио (Творческое Задание):</b>
                - <b>Повествование Взрослого:</b> "Давайте начнем с создания нашего собственного уровня..."
                - <b>Активность:</b> Дети рисуют и вырезают элементы уровня...

                [и так далее до {number_of_actions}-го действия]

                Сценарий должен окончиться разделом <b>Заключение:</b>

                Используй теги <b></b> для выделения важных элементов сценария, таких как названия разделов и ключевых моментов игры. 
                """

            client = openai.OpenAI(api_key=openai_api_key, http_client=httpx.Client())
            max_tokens = 2000
            completed_story = ""
            is_story_complete = False
            messages = [{"role": "user", "content": user_prompt}]
            while not is_story_complete:
                response = client.chat.completions.create(
                    model='gpt-4-1106-preview',
                    messages=messages
                )
                print(response)
                last_message = response.choices[0].message
                response_output = last_message.content if 'content' in last_message.dict() else ""
                completed_story += response_output
                if "Заключение:" in response_output or num_tokens_from_string(completed_story, 'cl100k_base') > max_tokens:
                    is_story_complete = True
                else:
                    messages.append({"role": "user", "content": "Продолжи историю."})
            return {"story": completed_story}

        except Exception as e:
            raise Exception(str(e))
