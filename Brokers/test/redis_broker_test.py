import pytest
from Brokers.redis_broker import RedisBroker
from redis import Redis


QUEUE_NAME = 'test_queue'

@pytest.fixture(autouse=True)
def cleanup():
    yield
    redis = Redis()
    redis.delete(QUEUE_NAME)

def test_init():
    broker = RedisBroker(QUEUE_NAME,0)
    assert(broker.key == QUEUE_NAME)
    assert(broker.timeout == 1)


def test_enqueue():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    broker.enqueue('Hello', 'Test1')
    
    assert(redis.llen(broker.key) == 1)

    broker.enqueue('Hello1', 'Test2')
    
    assert(redis.llen(broker.key) == 2)


def test_dequeue():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    res = broker.dequeue()
    assert(res == None)
    broker.enqueue('Hello', 'Test1')
    res = broker.dequeue()
    assert(res == b'Hello')
    assert(redis.llen(broker.key) == 0)

def test_queue_size():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    assert(redis.llen(broker.key) == broker.queue_size())
    broker.enqueue('Hello', 'Test1')
    assert(redis.llen(broker.key) == broker.queue_size())

def test_flush_queue():
    broker = RedisBroker(QUEUE_NAME,0)

    broker.enqueue('Hello', 'Test1')
    broker.enqueue('Hello1', 'Test2')
    
    broker.flush_queue()
    assert(broker.queue_size() == 0)


    

