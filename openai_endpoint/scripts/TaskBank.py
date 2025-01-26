
from Exceptions import *
from Constants import *

class TasksBank:
    def get_task_subst(self, age: int, gender: str) -> str:
        if gender not in [CHILD_GENDER_MALE, CHILD_GENDER_FEMALE]:
            raise IvalidGender
            
        
        if age in [6, 7, 8]:
            if gender == CHILD_GENDER_MALE:
                return DIFFICULTY_6_8_GENERAL + DIFFICULTY_6_8_BOYS
            else:
                return DIFFICULTY_6_8_GENERAL + DIFFICULTY_6_8_GIRLS
        elif age in [9, 10]:
            if gender == CHILD_GENDER_MALE:
                return DIFFICULTY_8_10_GENERAL + DIFFICULTY_8_10_BOYS
            else:
                return DIFFICULTY_8_10_GENERAL + DIFFICULTY_8_10_GIRLS
        elif age in [11, 12]:
            if gender == CHILD_GENDER_MALE:
                return DIFFICULTY_10_12_GENERAL + DIFFICULTY_10_12_BOYS
            else:
                return DIFFICULTY_10_12_GENERAL + DIFFICULTY_10_12_GIRLS
        else:
            raise UnsuportedAge
        