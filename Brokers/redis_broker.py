from Brokers.broker import Broker
from redis import Redis

class RedisBroker(Broker):

    def __init__(self, queue_id, timeout=1):
        super().__init__()
        self.redis = Redis()
        self.timeout = max(timeout,1) # min is 1 because broker does not support indefinite waits
        
        # Broker only supports one queue + corresponding logging queue to log all transactions and dlq
        self.key = queue_id
        self.logging_key = queue_id + '_logging_queue'
        self.dlq_key = queue_id + '_DLQ'
    
    def enqueue(self, task: str | bytes, task_id: str) -> None:
        self.redis.rpush(self.key,task)
        queued_message = f'{task_id} queued successfully'
        self.redis.rpush(self.logging_key, queued_message)
    
    def dequeue(self) -> str | bytes | None:
        task = self.redis.blpop([self.key],self.timeout)
        if task is None:
            return None
        return task[1]
        
    def queue_size(self) -> int:
        return self.redis.llen(self.key)

    def flush_queue(self) -> None:
        self.redis.ltrim(self.key,1,0)
    
    def log_success(self, task_id: str) -> None:
        success_message = f'{task_id} processed successfully'
        self.redis.rpush(self.logging_key, success_message)
    
    
    def log_failure(self, task_id: str) -> None:
        fail_message = f'{task_id} failed to process'
        self.redis.rpush(self.logging_key, fail_message)
    
    def process_failure(self, task: str | bytes, task_id: str) -> None:
        self.log_failure(task_id)
        self.redis.lpush(self.dlq_key, task)