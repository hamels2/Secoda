import pytest
from mock_broker import MockBroker
from TaskQueue.task_queue import TaskQueue

QUEUE_NAME = 'test_queue'


def task_function(a):
    return a+1


def test_enqueue():

    broker = MockBroker(QUEUE_NAME)
    task_queue = TaskQueue(broker)
    task_queue.enqueue(task_function, 0)
    
    assert(task_queue.get_length() == 1)

    task_queue.enqueue('Hello1', 'Test2')

    assert(task_queue.get_length() == 2)


def test_dequeue_success():

    broker = MockBroker(QUEUE_NAME)
    task_queue = TaskQueue(broker)
    task_queue.enqueue(task_function, 0)

    res = task_queue.dequeue()

    assert(res == 1)
    assert(task_queue.get_length() == 0)
    assert(len(broker.dlq) == 0)

def test_dequeue_failure():

    broker = MockBroker(QUEUE_NAME)
    task_queue = TaskQueue(broker)
    task_queue.enqueue(task_function, [])

    res = task_queue.dequeue()

    assert(res == None)
    assert(task_queue.get_length() == 0)
    assert(len(broker.dlq) == 1)





