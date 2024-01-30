from Brokers.broker import Broker
from redis import Redis

class RedisBroker(Broker):

    def __init__(self, qid, timeout=1):
        super().__init__()
        self.redis = Redis()
        self.key = qid
        self.timeout = max(timeout,1)
        self.logging_key = qid + '_logging_queue'
        self.dlq_key = qid + '_DLQ'
    
    def enqueue(self, task, task_id):

        self.redis.rpush(self.key,task)
        queued_message = f'{task_id} queued successfully'
        self.redis.rpush(self.logging_key, queued_message)
    
    def dequeue(self):
        task = self.redis.blpop([self.key],self.timeout)
        if task is None:
            return None
        return task[1]

        
    def queue_size(self):
        return self.redis.llen(self.key)

    def flush_queue(self):
        return self.redis.ltrim(self.key,1,0)
    
