from Brokers.redis_broker import RedisBroker
from TaskQueue.task_queue import TaskQueue
from count_task import count_words


if __name__ == "__main__":
    r = RedisBroker('test-queue-1')
    queue = TaskQueue(r)
    
    count = 0
    for num in range(4):
        queue.enqueue(count_words, "https://github.com")
        queue.enqueue(count_words, "https://news.ycombinator.com")
        queue.enqueue(count_words, "https://reddit.com")
        queue.enqueue(count_words, "https://nba.com")
        count += 4

    print(f"Enqueued {count} tasks")
    