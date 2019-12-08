import uuid
from datetime import datetime


class QueueItem:
    def __init__(self, type, body, attrs={}):
        self.id = uuid.uuid4()
        self.type = type
        self.body = body
        self.attrs = attrs
        self.timestamp = datetime.now()


class Queue:
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue

    def put(self, item):
        self.queue.put(item)

    def get(self):
        return self.queue.get()

    def empty(self, *args, **kwargs):
        return self.queue.empty()

    def task_done(self, *args, **kwargs):
        self.queue.task_done()
