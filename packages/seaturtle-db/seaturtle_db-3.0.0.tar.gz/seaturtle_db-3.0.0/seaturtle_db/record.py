import os
import sys
import pathlib
import importlib

from .exceptions import (
    RecordNotFoundError,
    RecordAlreadyExists
)

DEFAULT_DATA = "data = {}\n"

class RecordLabel:
    def __init__(self, data: bool) -> None:
        self._data = data

        self.properties = {'data': data}

    @property
    def data(self) -> bool: return self._data

    @data.setter
    def data(self, value: bool) -> None:
        self._data = value
        self.properties['data'] = self._data

    @property
    def is_valid(self) -> bool:
        values = list(self.properties.values())
        return any(values)

    def __iter__(self):
        return iter(self.properties.items())


class Record:
    def __init__(
            self,
            database: str,
            name: str,
            data: dict
    ) -> None:
        self.database = database
        self.db_location = pathlib.Path(sys.path[0]) / self.database
        self.importable = database.replace('/', '.')

        self.name = name
        self.file = name + '.py'

        self.data = data

    @property
    def exists(self) -> bool:
        return (self.db_location / self.file).exists()

    @staticmethod
    def _make_write_data(*, data: dict = None):
        text = ""
        text += (f'{data = }' if data else DEFAULT_DATA) + '\n'

        return text

    @classmethod
    def create(cls, database: str, name: str, *, overwrite: bool = False, data: dict = None) -> "Record":
        db_location = pathlib.Path(sys.path[0]) / database
        file = name + '.py'

        if (db_location / file).exists():
            if overwrite:
                with open(db_location / file, 'w') as record:
                    record.write(cls._make_write_data(
                        data=data
                    ))

                return cls(database, name, data)

            raise RecordAlreadyExists(
                f"The specified record {name!r} already exists and `overwrite` was set to False"
            )

        with open(db_location / file, 'a') as record:
            record.write(cls._make_write_data(
                data=data
            ))

        return cls(database, name, data)

    @classmethod
    def fetch(cls, database: str, name: str) -> "Record":
        db_location = pathlib.Path(sys.path[0]) / database
        importable = database.replace('/', '.')

        if not (
            db_location /
            (name + '.py')
        ).exists():
            raise RecordNotFoundError(
                f"The specified record {name!r} was not found in the database directory {db_location!r}"
            )

        module = getattr(__import__(f'{importable}.{name}'), name)
        importlib.reload(module)

        return cls(database, name, module.data)

    def read(self, record_label: RecordLabel) -> list:
        module = getattr(__import__(f'{self.importable}.{self.name}'), self.name)
        importlib.reload(module)

        results = [attr for attr, on in record_label if on]

        return [getattr(module, attr) for attr in results]

    def update(self) -> None:
        if not self.exists:
            raise RecordNotFoundError(
                f"The specified record {self.name!r} was not found in the database directory {self.db_location!r}"
            )

        with open(self.db_location / self.file, 'w') as record:
            record.write(self._make_write_data(
                data=self.data
            ))

    def delete(self) -> None:
        if not self.exists:
            raise RecordNotFoundError(
                f"The specified record {self.name!r} was not found in the database directory {self.db_location!r}"
            )

        os.remove(self.db_location / self.file)
