from enum import Enum
import uuid
from typing import Any

class TaskStatus(Enum):
    QUEUED: 1
    SUCCESS: 2
    FAILED: 3

class Task(object):

    def __init__(self, func, *args):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.status = None
    
    def update_status(self, status: TaskStatus) -> None:
        self.status = status

    def process_task(self) -> Any:
        return self.func(*self.args)
