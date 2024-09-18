import os
import sys
import pathlib
import importlib

from .exceptions import (
    DatabaseNotFoundError,
    RecordNotFoundError,
    RecordAlreadyExists
)

class Database:
    def __init__(
            self,
            dir_name: str,
            **kwargs
    ) -> None:
        self.dir_name = dir_name.split('/', 1)[-1]
        self.create_if_not_exists = kwargs.get('create_if_not_exists', True) and kwargs.get('cine', True)

        self.dir_as_importable = self.dir_name.replace('/', '.')

        self.use_dir = pathlib.Path(sys.path[0]) / self.dir_name

        with open('hello.txt', 'w') as f: f.write(str(self.use_dir))

        self.verify_database_existence()

    def verify_database_existence(self) -> None:
        """Verifies the existence of the database directory, and creates it if it doesn't exist and
        `Database.create_if_not_exists` has been set to False.

        :raises DatabaseNotFoundError: If the database directory does not exist and `Database.create_if_not_exists` has been set to False
        """

        if not self.use_dir.exists():
            if self.create_if_not_exists:
                return os.makedirs(self.use_dir)

            raise DatabaseNotFoundError(
                f"The specified database directory {self.dir_name!r} was not found and the `create_if_not_exists` was set to False."
            )

    def read_record(self, record: str) -> dict:
        if not (self.use_dir / f'{record}.py').exists():
            raise RecordNotFoundError(
                f"The specified record {record!r} was not found in the database directory {self.dir_as_importable!r}"
            )

        module =  getattr(__import__(f'{self.dir_as_importable}.{record}'), record)
        importlib.reload(module)

        return module.data

    def create_record(self, record: str, **kwargs) -> None:
        overwrite_if_exists: bool = kwargs.get('overwrite_if_exists', True) and kwargs.get('oie', True) and kwargs.get('overwrite', True)

        if (self.use_dir / f'{record}.py').exists():
            if overwrite_if_exists:
                with open(self.use_dir / f'{record}.py', 'w') as record:
                    record.write('data = {}')

                return

            raise RecordAlreadyExists(
                f"The specified record {record!r} already exists and `overwrite` was set to False"
            )

        with open(self.use_dir / f'{record}.py', 'w') as record:
            record.write('data = {}')

        return

    def update_record(self, record: str, data: dict) -> None:
        if not (self.use_dir / f'{record}.py').exists():
            raise RecordNotFoundError(
                f"The specified record {record!r} was not found in the database directory {self.dir_as_importable!r}"
            )

        with open(self.use_dir / f'{record}.py', 'w') as record:
            record.write(f'{data = }')

    def delete_record(self, record: str) -> None:
        if not (self.use_dir / f'{record}.py').exists():
            raise RecordNotFoundError(
                f"The specified record {record!r} was not found in the database directory {self.dir_as_importable!r}"
            )

        os.remove(self.use_dir / f'{record}.py')

