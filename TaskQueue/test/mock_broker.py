from Brokers.broker import Broker

class MockBroker(Broker):
    def __init__(self, qid):
        super().__init__()
        self.queue = []
        self.dlq = []
    
    def enqueue(self, task, task_id):
        print( f'{task_id} queued successfully')
        self.queue.append(task)
    
    def dequeue(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

        
    def queue_size(self):
        return len(self.queue)

    def flush_queue(self):
        self.queue = []
    
    def log_success(self, task_id: str):
        print(f'{task_id} processed successfully')
    
    
    def log_failure(self, task_id: str):
        print(f'{task_id} failed to process')
    
    def process_failure(self, task, task_id):
        print(f'{task_id} failed to process')
        self.dlq.append(task)