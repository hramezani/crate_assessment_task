from datetime import date
from uuid import uuid4

from sqlalchemy import Boolean, Column, Date, Integer, String

from db import Base
from db.utils import get_cleaner


def gen_key():
    return str(uuid4())


class CalendarDate(Base):
    __tablename__ = 'calendar_date'

    id = Column(String, primary_key=True, default=gen_key)
    service_id = Column(Integer)
    date = Column(Date)
    exception_type = Column(Integer)


class Calendar(Base):
    __tablename__ = 'calendar'

    id = Column(String, primary_key=True, default=gen_key)
    service_id = Column(Integer)
    monday = Column(Boolean)
    tuesday = Column(Boolean)
    wednesday = Column(Boolean)
    thursday = Column(Boolean)
    friday = Column(Boolean)
    saturday = Column(Boolean)
    sunday = Column(Boolean)
    start_date = Column(Date)
    end_date = Column(Date)


class Route(Base):
    __tablename__ = 'route'

    id = Column(String, primary_key=True, default=gen_key)
    route_id = Column(String)
    agency_id = Column(Integer)
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_type = Column(Integer)
    route_color = Column(String)
    route_text_color = Column(String)
    route_desc = Column(String)


class Shape(Base):
    __tablename__ = 'shape'

    id = Column(String, primary_key=True, default=gen_key)
    shape_id = Column(Integer)
    shape_pt_lat = Column(String)
    shape_pt_lon = Column(String)
    shape_pt_sequence = Column(Integer)


class StopTime(Base):
    __tablename__ = 'stop_time'

    id = Column(String, primary_key=True, default=gen_key)
    trip_id = Column(Integer)
    arrival_time = Column(String)
    departure_time = Column(String)
    stop_id = Column(String)
    stop_sequence = Column(Integer)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    stop_headsign = Column(String)


class Stop(Base):
    __tablename__ = 'stop'

    id = Column(String, primary_key=True, default=gen_key)
    stop_id = Column(String)
    stop_code = Column(String)
    stop_name = Column(String)
    stop_desc = Column(String)
    stop_lat = Column(String)
    stop_lon = Column(String)
    location_type = Column(Integer)
    parent_station = Column(String)
    wheelchair_boarding = Column(Boolean)
    platform_code = Column(String)
    zone_id = Column(String)


class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column(String, primary_key=True, default=gen_key)

    from_stop_id = Column(String)
    to_stop_id = Column(String)
    transfer_type = Column(Integer)
    min_transfer_time = Column(Integer)
    from_route_id = Column(String)
    to_route_id = Column(String)
    from_trip_id = Column(String)
    to_trip_id = Column(String)


class Trip(Base):
    __tablename__ = 'trip'

    id = Column(String, primary_key=True, default=gen_key)

    route_id = Column(String)
    service_id = Column(Integer)
    trip_id = Column(String)
    trip_headsign = Column(String)
    trip_short_name = Column(String)
    direction_id = Column(Integer)
    block_id = Column(Integer)
    shape_id = Column(Integer)
    wheelchair_accessible = Column(Boolean)
    bikes_allowed = Column(Boolean)


models = {
    'CalendarDate': CalendarDate,
    'Calendar': Calendar,
    'Route': Route,
    'Shape': Shape,
    'StopTime': StopTime,
    'Stop': Stop,
    'Transfer': Transfer,
    'Trip': Trip,
}


def get_model(model_name):
    return models.get(model_name)


def clean_field(value, field_type, default=None):
    cleaner = get_cleaner(field_type)
    if cleaner:
        value = cleaner(value, default)
    return value


def clean_fields(model, fields, default=None):
    cleaned_row = {}
    for name, value in fields.items():
        field = getattr(model, name)
        field_type = str(field.type)
        value = clean_field(value, field_type, default)
        cleaned_row[name] = value
    return cleaned_row


def clean_row(model, row, columns, default='null'):
    cleaned_row = []
    for index, col_name, in enumerate(columns):
        field = getattr(model, col_name)
        field_type = str(field.type)
        value = str(clean_field(row[index], field_type, default))
        if field_type in ('VARCHAR', 'DATE') and value != 'null':
            value = f'\'{value}\''
        cleaned_row.append(value)
    return cleaned_row
