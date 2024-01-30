from Brokers.redis_broker import RedisBroker

from TaskQueue.task_queue import TaskQueue


def worker():
    r = RedisBroker('test-queue-1')
    queue = TaskQueue(r)
    if queue.get_length() > 0:
        queue.dequeue()
    else:
        print("No tasks in the queue")


if __name__ == "__main__":
    worker()