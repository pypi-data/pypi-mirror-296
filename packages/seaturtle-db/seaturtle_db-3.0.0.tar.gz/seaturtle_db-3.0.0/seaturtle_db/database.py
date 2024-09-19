import os
import sys
import pathlib
import importlib

from .exceptions import (
    DatabaseNotFoundError,
    RecordNotFoundError,
    RecordAlreadyExists
)

from .record import Record

class Database:
    def __init__(
            self,
            db_name: str,
            **kwargs
    ) -> None:
        self.db_name = db_name
        self.create_if_not_exists = kwargs.get('create_if_not_exists', True) and kwargs.get('cine', True)

        self.db_location = pathlib.Path(sys.path[0]) / self.db_name

        self.verify_database_existence()

        self.records: list[Record] = []

    def verify_database_existence(self) -> None:
        """Verifies the existence of the database directory, and creates it if it doesn't exist and
        `Database.create_if_not_exists` has been set to False.

        :raises DatabaseNotFoundError: If the database directory does not exist and `Database.create_if_not_exists` has been set to False
        """

        if not self.db_location.exists():
            if self.create_if_not_exists:
                return os.makedirs(self.db_location)

            raise DatabaseNotFoundError(
                f"The specified database directory {self.db_location!r} was not found and the `create_if_not_exists` was set to False."
            )

    def read_record(self, name: str) -> Record:
        record = Record.read(
            self.db_name,
            name
        )

        for rec in self.records:
            if rec.name != name:
                break
        else:
            self.records.append(record)

        return record

    def create_record(self, name: str, *, overwrite: bool = False, data: dict = {}) -> Record:
        record = Record.create(
            self.db_name,
            name,
            overwrite=overwrite,
            data=data
        )

        for rec in self.records:
            if rec.name != name:
                break
        else:
            self.records.append(record)

        return record

    def update_record(self, name: str, data: dict) -> None:
        record = Record.fetch(
            self.db_name,
            name
        )

        record.data = data

        record.update()

    def delete_record(self, name: str) -> None:
        record = Record.fetch(
            self.db_name,
            name
        )

        record.delete()
