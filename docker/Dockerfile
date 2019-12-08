FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./crate_assessment/ /code/crate_assessment/
COPY ./docker/wait-for-it.sh /code/
RUN mkdir /data
