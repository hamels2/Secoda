class Broker:

    def enqueue(self, task, task_id):
        """
        Puts a task onto the queue
        :type task: str
        :type task_id: str
        """
        pass

    def dequeue(self):
        """
        Gets a task from the queue
        :return: task message
        """
        pass

    def queue_size(self):
        """
        :return: the amount of tasks in the queue
        """
        pass

    def flush_queue(self):
        """
        Flushes the queue of any tasks
        """
        pass

    def log_success(self, task_id: str):
        """
        :type task_id: str
        Logs a success message for given task
        """
        pass

    
    
    def log_failure(self, task_id: str):
        """
        :type task_id: str
        Logs a failure message for given task
        """
        pass
    
    def process_failure(self, task, task_id):
        """
        :type task: str
        :type task_id: str
        Logs a success message for given task and sends task to DLQ
        """
        pass


  