import os

from sqlalchemy import create_engine
from sqlalchemy.ext import declarative
from sqlalchemy.orm import sessionmaker


engine = create_engine(
    os.environ.get('CRATE_DB_ADDRESS', 'crate://crate@localhost:4200')
)
Base = declarative.declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


def create_all_table():
    Base.metadata.create_all(engine)


def drop_all_table():
    Base.metadata.drop_all(engine)
