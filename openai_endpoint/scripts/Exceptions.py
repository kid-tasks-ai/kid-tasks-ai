class TasksDBException(Exception):
    pass

class UnsuportedAge(TasksDBException):
    pass

class IvalidGender(TasksDBException):
    pass