import os
import openai
from pydantic import BaseModel
from Constants import *
from Exceptions import *
from TaskBank import TasksBank
import json
import sys


# Configure your proxy
openai_api_key = os.getenv("OPENAI_API_KEY")

task_bank = None
try:
    task_bank = TasksBank()
except TasksDBException as e:
    print("Task BANK initialization failed: {e}", file=sys.stderr)


class TasksGenerator(BaseModel):
    @staticmethod
    def __build_prompt(payload: str) -> dict:
        """
        Builds prompt based in settings in json string

        :param payload: string with json received in http
        :return: {"prompt": "", "error": ""}. If generation failed -> tasks is empty, error contains fail reason
        """
        return_struct = {"prompt": "", "error": ""}

        try:
            gen_settings = json.loads(payload)
        except json.JSONDecodeError:
            return_struct["error"] = "Unable parse json: \"{payload}\""
            return return_struct
        except:
            return_struct["error"] = "Unknown json parse error: \"{payload}\""
            return return_struct

        user_prompt = "" 
        try:
            child_desc = gen_settings[CHILD_DESCRIPTION]
            user_prompt += PROMPT_CHILD_DESCRIPTION.format(
                age=child_desc[CHILD_AGE],
                gender= " летней девочки" if child_desc[CHILD_GENDER] == CHILD_GENDER_FEMALE else " летнего мальчика",
                interests=child_desc[CHILD_INTERESTS],
                materials=DEFAULT_INVENTORY
            )

            tasks_desc = gen_settings[TASKS_DESCRIPTION]
            user_prompt += PROMPT_TASKS_DESCRIPTION_BEGINNING

            # generate chore tasks only if chore field exists and array not empty
            if CHORE_TASKS in tasks_desc.keys() and tasks_desc[CHORE_TASKS]:
                user_prompt += PROMPT_TASKS_DESCRIPTION_CHORE.format(
                    chore_number=len(tasks_desc[CHORE_TASKS]),
                    chore_activity=tasks_desc[CHORE_TASKS]
                )

            # if topic for creative tasks not provided, use child interests
            if not tasks_desc[CREATIVE_TASKS][CREATIVE_TASKS_TOPICS]:
                tasks_desc[CREATIVE_TASKS][CREATIVE_TASKS_TOPICS].append(child_desc[CHILD_INTERESTS])

            user_prompt += PROMPT_TASKS_DESCRIPTION_CREATIVE.format(
                creative_number=tasks_desc[CREATIVE_TASKS][CREATIVE_TASKS_NUMBER],
                creative_topics=tasks_desc[CREATIVE_TASKS][CREATIVE_TASKS_TOPICS]
            )
            
            if task_bank:
                user_prompt += PROMPT_DIFFICULTY_EXAMPLES.format(
                    tasks_examples=task_bank.get_task_subst(child_desc[CHILD_AGE], child_desc[CHILD_GENDER])
                )

            user_prompt += PROMPT_STRUCTURE

        except KeyError as e:
            return_struct["error"] = "Invalid json structure: \"{e}\""
            return return_struct
        except IvalidGender:
            return_struct["error"] = "Invalid gender value"
            return return_struct
        except UnsuportedAge:
            return_struct["error"] = "Invalid age value. Age should be from 6 to 12 inclusive"
            return return_struct    
    
        return_struct["prompt"] = user_prompt
        return return_struct

        
    @staticmethod
    def get_tasks(payload: str) -> dict:
        """
        Generates tasks based on provided settings

        :param payload: string with json received in http
        :return: {"tasks": "", "error": ""}. If generation failed -> tasks is empty, error contains fail reason
        """
        try:
            prompt = TasksGenerator.__build_prompt(payload)
            if not prompt["prompt"]:
                return {"tasks": "", "error": prompt["error"]}
            
            client = openai.OpenAI(api_key=openai_api_key)
            messages = [{"role": "user", "content": prompt["prompt"]}]
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                response_format={"type": "json_object"},
                messages=messages
            )
            response_output = response.choices[0].message.content
            return {"tasks": response_output, "error": ""}

        except Exception as e:
            return {"tasks": "", "error": "Error while tasks generation: " + str(e)}
