import os
import time
import uuid
from datetime import datetime
from multiprocessing import Manager, Pipe, Pool, current_process
from pathlib import Path

from db import create_all_table, drop_all_table
from handlers import (DBHandler, DBPrepHandler, DefaultFileHandler,
                      DefaultPrepHandler, ORMHandler)
from queues import Queue, QueueItem
from utils import get_files_list
from workers import FileWorker, Worker


file_model_map = {  # filename: (model_name, type, batch_size)
    'calendar_dates.txt': ('CalendarDate', 'orm', 2000),
    'calendar.txt': ('Calendar', 'orm', 200),
    'routes.txt': ('Route', 'orm', 200),
    'shapes.txt': ('Shape', 'db', 20000),
    'stop_times.txt': ('StopTime', 'db', 20000),
    'stops.txt': ('Stop', 'orm', 500),
    'transfers.txt': ('Transfer', 'db', 20000),
    'trips.txt': ('Trip', 'orm', 2000),
}

if __name__ == '__main__':
    drop_all_table()
    create_all_table()

    # Create queues
    file_queue = Queue('FileQueue', Manager().Queue())
    prep_queue = Queue('PrepQueue', Manager().Queue())
    db_queue = Queue('DBQueue', Manager().Queue())

    # Create processes
    pool = Pool()
    default_file_handler = DefaultFileHandler()
    for i in range(1, 3):
        file_worker = FileWorker(f'File Worker{i}', file_queue)
        file_worker.register_handler(default_file_handler)
        file_worker.register_result_queue(prep_queue)
        pool.apply_async(file_worker.process)

    default_prep_handler = DefaultPrepHandler()
    db_prep_handler = DBPrepHandler()
    for i in range(1, 3):
        prep_worker = Worker(f'Prep Worker{i}', prep_queue)
        prep_worker.register_handler(default_prep_handler)
        prep_worker.register_handler(db_prep_handler)
        prep_worker.register_result_queue(db_queue)
        pool.apply_async(prep_worker.process)

    orm_handler = ORMHandler()
    db_handler = DBHandler()
    for i in range(1, 5):
        db_worker = Worker(f'DB Worker{i}', db_queue)
        db_worker.register_handler(orm_handler)
        db_worker.register_handler(db_handler)
        pool.apply_async(db_worker.process)

    pool.close()

    # Read files name from data directory and put an item per file
    for path in get_files_list(Path('data')):
        file_info = file_model_map.get(path.name)
        if file_info is not None:
            model, type, batch_size = file_info
            item = QueueItem(
                type,
                {'path': path},
                {'model': model, 'batch_size': batch_size}
            )
            file_queue.put(item)

    pool.join()
