import pytest
from Brokers.redis_broker import RedisBroker
from redis import Redis


QUEUE_NAME = 'test_queue'

@pytest.fixture(autouse=True)
def cleanup():
    yield
    redis = Redis()
    redis.delete(QUEUE_NAME)
    redis.delete(QUEUE_NAME + '_logging_queue')
    redis.delete(QUEUE_NAME + '_DLQ')

def test_init():
    broker = RedisBroker(QUEUE_NAME,0)
    assert(broker.key == QUEUE_NAME)
    assert(broker.logging_key == QUEUE_NAME + '_logging_queue')
    assert(broker.timeout == 1)
    assert(broker.dlq_key == QUEUE_NAME + '_DLQ')


def test_enqueue():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    broker.enqueue('Hello', 'Test1')
    
    assert(redis.llen(broker.key) == 1)
    assert(redis.llen(broker.logging_key) == 1)
    assert(redis.llen(broker.dlq_key) == 0)

    broker.enqueue('Hello1', 'Test2')
    
    assert(redis.llen(broker.key) == 2)
    assert(redis.llen(broker.logging_key) == 2)
    assert(redis.llen(broker.dlq_key) == 0)


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

def test_log_success():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    broker.log_success('Test1')
    assert(redis.llen(broker.logging_key) == 1)
    msg = redis.blpop(broker.logging_key)[1]
    assert(msg == b'Test1 processed successfully')

def test_log_failure():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    broker.log_failure('Test1')
    assert(redis.llen(broker.logging_key) == 1)
    msg = redis.blpop(broker.logging_key)[1]
    assert(msg == b'Test1 failed to process')

def test_process_failure():
    redis = Redis()
    broker = RedisBroker(QUEUE_NAME,0)
    broker.process_failure('hello','Test1')
    assert(redis.llen(broker.logging_key) == 1)
    msg = redis.blpop(broker.logging_key)[1]
    assert(msg == b'Test1 failed to process')

    assert(redis.llen(broker.dlq_key) == 1)
    msg = redis.blpop(broker.dlq_key)[1]
    assert(msg == b'hello')


    

