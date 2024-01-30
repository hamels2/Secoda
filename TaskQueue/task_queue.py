from Brokers.broker import Broker
from TaskQueue.task import Task
from typing import Any

import pickle


class TaskQueue(object):
    def __init__(self, broker: Broker):
        self.broker = broker

    def enqueue(self, func, *args) -> str:
        task = Task(func, *args)
        serialized_task = pickle.dumps(task, protocol=pickle.HIGHEST_PROTOCOL)
        self.broker.enqueue(serialized_task, task.id)
        return task.id

    def dequeue(self) -> Any:
        serialized_task = self.broker.dequeue()
        task = pickle.loads(serialized_task)
        
        try:
            response = task.process_task()
            self.broker.log_success(task.id)
            return response
        
        except:
            print('Processing task failed')
            task.update_status(0)
            serialized_task = pickle.dumps(task, protocol=pickle.HIGHEST_PROTOCOL)
            self.broker.process_failure(serialized_task, task.id)
            return None

    def get_length(self) -> int:
        return self.broker.queue_size()
    
        