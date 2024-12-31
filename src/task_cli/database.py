import sys
import json
from os import path
from typing import TypeVar
from task_cli.utils import deserialize, serialize

T = TypeVar("T")


class Database:
    def __init__(self, file_path: str, document: type[T]):
        self.data = document()
        self.__file_path = file_path
        self.__load(file_path)

    @property
    def document(self) -> type[T]:
        return self.data

    @property
    def file_path(self) -> str:
        return self.__file_path

    def read(self):
        return self.data

    def commit(self):
        with open(self.__file_path, 'w') as file:
            file.write(serialize(self.data))

    def __load(self, file_path: str):
        try:
            if not path.exists(file_path):
                with open(file_path, 'w') as file:
                    self.commit()
                    return

            with open(file_path, 'r') as file:
                self.data = deserialize(into=self.data.__class__, data=file.read())
        except json.JSONDecodeError:
            print('INFO: Invalid DB state - will create an empty document.')
            self.commit()
        except Exception as error:
            print(
                f'An error occurred while setting up the database: {error}.',
                file=sys.stderr,
            )
            self.commit()
