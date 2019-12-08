import csv

from db import session
from db.models import clean_fields, clean_row, gen_key, get_model


class Handler:
    def before_handle(self, item):
        pass

    def after_handle(self, item):
        pass

    def handle(self, item):
        self.before_handle(item)
        result = self._handle(item)
        self.after_handle(item)
        return result

    def _handle(self, item):
        raise NotImplementedError


class DefaultFileHandler(Handler):
    """
    Reads file lines and create a new item with the line number equals
    to batch_size.
    """
    name = 'DefaultFileHandler'
    type = 'default'

    def before_handle(self, item):
        self.file_path = item.body['path']
        self.file_name = item.body['path'].name
        print(f'Reading file {self.file_name} started by {self.name}.')

    def _get_columns(self, line):
        return [c.strip().strip('"') for c in line.strip().split(',')]

    def _handle(self, item):
        batch = []
        counter = 0
        attrs = item.attrs
        batch_size = attrs['batch_size']

        with open(self.file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            # Get columns from first line
            attrs['columns'] = next(reader)
            for line in reader:
                batch.append(line)
                counter += 1
                if counter == batch_size:
                    yield (item.type, {'rows': batch}, attrs)
                    batch = []
                    counter = 0
            yield (item.type, {'rows': batch}, attrs)

    def after_handle(self, item):
        print(f'Reading file {self.file_name} finished.')


class DefaultPrepHandler(Handler):
    """
    Cleans rows and creates objects to save by ORM.
    """
    name = 'DefaultPrepHandler'
    type = 'default'

    def _handle(self, item):
        columns = item.attrs['columns']
        model = get_model(item.attrs['model'])
        rows = item.body['rows']

        objects = [
            model(**clean_fields(model, dict(zip(columns, row))))
            for row in rows
        ]
        return (item.type, {'objects': objects}, item.attrs)


class DBPrepHandler(Handler):
    """
    Cleans rows and creates values for insert to db.
    """
    name = 'DefaultPrepHandler'
    type = 'db'

    def _handle(self, item):
        columns = item.attrs['columns']
        model = get_model(item.attrs['model'])
        rows = item.body['rows']
        values = []

        for row in rows:
            row = [f'\'{gen_key()}\''] + clean_row(model, row, columns)
            values.append('(%s)' % ','.join(row))

        return (item.type, {'values': values}, item.attrs)


class ORMHandler(Handler):
    """
    Get ORM object and save them in bulk.
    """
    name = 'DefaultDBHandler'
    type = 'default'

    def _handle(self, item):
        columns = item.attrs['columns']
        objects = item.body['objects']

        try:
            session.bulk_save_objects(objects)
            session.commit()
        except Exception as e:
            print(f'Error in bulk save {item.id}')


class DBHandler(Handler):
    """
    Get valued and insert them in bulk to db.
    """
    name = 'DefaultDBHandler'
    type = 'db'

    def _handle(self, item):
        values = item.body['values']
        model = get_model(item.attrs['model'])

        try:
            session.execute('insert into %s values %s' % (
                model.__tablename__, ','.join(values)
            ))
            session.commit()
        except Exception as e:
            print(f'Error in bulk insert {item.id}')
