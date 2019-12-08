from queues import QueueItem


class Worker:
    """
    Get an item from queue.
    Process item by handler.
    Put processed item on result queues(0 or multiple queue).
    """
    def __init__(self, name, queue):
        self.name = name
        self.queue = queue
        self.result_queues = []
        self.handlers = {}

    def register_handler(self, handler):
        """
        Register handler to process item.
        """
        self.handlers[handler.type] = handler
        print(f'Hander {handler.name} registered for worker {self.name}.')

    def register_result_queue(self, queue):
        """
        Register queue for processed item.
        """
        self.result_queues.append(queue)
        print(f'Result queue {queue.name} registered for worker {self.name}.')

    def get_handler(self, item):
        """
        Returns handler base of item type.
        """
        if item.type in self.handlers:
            return self.handlers[item.type]
        return self.handlers.get('default', None)

    def get_item(self):
        """
        Receive an item from queue.
        """
        item = self.queue.get()
        print(f'Item {item.id} received by {self.name}')
        return item

    def process(self):
        while True:
            item = self.get_item()
            result = self._process(item)
            self._process_result(item, result)
            self._finish_process(item, result)

    def _process(self, item):
        handler = self.get_handler(item)
        if handler:
            return handler.handle(item)
        else:
            return None

    def _process_result(self, item, result):
        if self.result_queues and result:
            type, body, attrs = result
            for queue in self.result_queues:
                item = QueueItem(type, body, attrs)
                queue.put(item)

    def _finish_process(self, item, result):
        self.queue.task_done()
        print(f'Item {item.id} finished by {self.name}')


class FileWorker(Worker):
    def _process(self, item):
        handler = self.get_handler(item)
        if handler:
            for result in handler.handle(item):
                type, body, attrs = result
                if self.result_queues:
                    for queue in self.result_queues:
                        item = QueueItem(type, body, attrs)
                        queue.put(item)

        return None
