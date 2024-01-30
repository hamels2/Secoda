# Concurrent task queue

Implementation of a concurrent task queue with Redis as a broker

## Setup

Developed on WSL Ubuntu, steps should be applicable to any unix based system

Install dependencies: pip install -r ./requirements.txt
Install redis-server: sudo apt-get install redis-server
Start Redis server: sudo service redis-server start


## Run

I created a set of files to show the concurrent capabilities of the task queue:


count_task.py Stores the task being preformed, it counts the given words in a webpage
spawn_jobs.py Emulates a set of clients writing to the task queue
workers.py Emulates a worker reading from task queue/processing task
spawn_workers.py Emulates concurrent workers by starting a multiprocessing loop for x number of workers consuming from the queue

To run:
sudo service redis-server start
in one terminal run python spawn_job.py to enqueue tasks
then in another terminal run spawn_workers.py to consume tasks concurrently, at any point you can add more tasks by re-running spawn_jobs.py. If 
spawn_workers is left without tasks for a while, it'll crash.
Alternatively to consume from queue one at a time run worker.py


## Tests:

run sudo service redis-server start
run python3 -m pytest
