=======================
Crate Assessment Task
=======================

Description
##############
This project is written in ``Python3.7`` like a pipeline. data(file lines)
input from one side of the pipeline and written in Database at the end of the
pipeline.

The pipeline is created  by 3 components:

Queue
********
The queue is like a pipe and used for sending/receiving items from/to workers.


Worker
*******
The worker receives an item from the queue and process it and will send them
to other queues for the next phase.

Handler
*******
The handler is used to process the item in the worker. each worker can have
multiple handlers for different kinds of items.

Here is the workflow:

1. File workers receive the file name.
2. File workers open the file and read the file lines and create an item with
   the line number of `batch_size`, then create an item for the next
   step(Preparation).
3. Preparation workers receive items from the previous step and clean the data
   for the next step. then create an item for the next step(Save).
4. DB workers receive items from the previous step and write them to the
   Database.

Run
#####

1. Clone the project::

    $ git clone https://github.com/hramezani/crate_assessment_task.git

2. Go to project directory::

    $ cd crate_assessment_task

3. Download VBB GTFS dataset from
     https://daten.berlin.de/datensaetze/vbb-fahrplandaten-gtfs and extract
     them to ``data`` directory.

4. Create virtual environment and enable it::

    $ virtualenv --python /usr/local/bin/python3.7 env
    $ source env/bin/activate

5. Install requirements::

    $ pip install -r requirements.txt

6. Set Database address. (default is ``crate://localhost:4200``). if your
   database is running on default port you can ignore this step::

    $ export CRATE_DB_ADDRESS=<db_address>

7. Run the project by::

    $ python crate_assessment/runner.py

You can go to dashboard (http://localhost:4200/) and check the numbers in
table section of dashboard.

**Every time project runs it will remove all the tables and recreate them.**


Run By Docker
##############

1. Clone the project::

    $ git clone https://github.com/hramezani/crate_assessment_task.git

2. Go to project directory::

    $ cd crate_assessment_task

3. Download VBB GTFS dataset from
   https://daten.berlin.de/datensaetze/vbb-fahrplandaten-gtfs and extract
   them to ``data`` directory.

4. Build docker image::

    $ docker build -f docker/Dockerfile -t crate_test .

5. Run docker compose::

    $ docker-compose -f docker/docker-compose.yml up

Run Tests
##############
You can run all the tests by::

    $ python -m unittest discover tests


Why I Chose this solution
###########################
This solution is flexible it means we can:

* Add stage to pipeline.
* Change/Add the handler of worker.
* Add another queue as result queue. it means one stage produce item for
  multiple stage.
* Change number of processes for each stage.
* Change type of queue.
* ...

This is also has good performance because we have multiple process for each
stage.

What are missed
######################

* Complete the tests.
* Better error handling and logging.
* Handle Geo data.
* Better performance specially in database worker.
* Better handling of configuration like db address, batch size,
  number of processes ,...
* ...
