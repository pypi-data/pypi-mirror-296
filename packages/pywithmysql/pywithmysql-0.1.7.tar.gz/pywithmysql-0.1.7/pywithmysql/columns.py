from typing import Any
from pywithmysql.types import TypesEnum


class Column:
    def __init__(self,
                 name: str,
                 type_: TypesEnum,
                 nullable: bool = False,
                 max_length: int = 255,
                 default: Any = None,
                 unique: bool = False
                ) -> None:
        """
        Create column to your table
        :param name: str your Column name
        :param type_: import types (from pywithmysql.types import IntegerField, CharField, .......)
        :param nullable: bool
        :param max_length: int
        """
        self.__name = name
        self.__type = type_
        self.__nullable = nullable
        self.__max_length = max_length
        self.__default = default
        self.__unique = unique

    @property
    def get_all_data(self) -> dict:
        """
        Get all data from Column
        :return: dict (with data from Column)
        """
        return {
            "name": self.__name,
            "type": self.__type.__str__(self),
            "nullable": self.__nullable,
            "max_length": self.__max_length,
            "default": self.__default,
            "unique": self.__unique,
        }

