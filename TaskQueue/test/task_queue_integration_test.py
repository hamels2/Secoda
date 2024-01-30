import pytest

from Brokers.redis_broker import RedisBroker
from redis import Redis
from TaskQueue.task_queue import TaskQueue
from TaskQueue.task import Task


QUEUE_NAME = 'test_queue'

def task_function(a):
    return a+1

@pytest.fixture(autouse=True)
def cleanup():
    yield
    redis = Redis()
    redis.delete(QUEUE_NAME)
    redis.delete(QUEUE_NAME + '_logging_queue')
    redis.delete(QUEUE_NAME + '_DLQ')



def test_enqueue_dequeue_success():

    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    queue = TaskQueue(broker)
    queue.enqueue(task_function, 0)
    
    assert(redis.llen(broker.key) == 1)
    assert(redis.llen(broker.logging_key) == 1)
    assert(redis.llen(broker.dlq_key) == 0)
    
    assert(queue.get_length() == 1)

    res = queue.dequeue()
    assert(res == 1)
    assert(redis.llen(broker.key) == 0)
    assert(redis.llen(broker.logging_key) == 2)
    assert(redis.llen(broker.dlq_key) == 0)


def test_enqueue_dequeue_failure():
    
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    queue = TaskQueue(broker)
    queue.enqueue(task_function, [])
    
    assert(redis.llen(broker.key) == 1)
    assert(redis.llen(broker.logging_key) == 1)
    assert(redis.llen(broker.dlq_key) == 0)
    
    assert(queue.get_length() == 1)

    res = queue.dequeue()
    assert(res == None)
    assert(redis.llen(broker.key) == 0)
    assert(redis.llen(broker.logging_key) == 2)
    assert(redis.llen(broker.dlq_key) == 1)




    

