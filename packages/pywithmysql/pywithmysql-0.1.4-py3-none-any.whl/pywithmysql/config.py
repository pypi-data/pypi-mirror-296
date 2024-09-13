from pywithmysql.searchconfig import get_or_create_config


class DataBaseConfig:
    def __init__(self) -> None:
        """
        Get data from .env to connect
        """
        data = get_or_create_config()
        self.__host = data.get('host')
        self.__port = data.get('port')
        self.__password = data.get('password')
        self.__user = data.get('user')
        self.__db_name = data.get("db_name")

    @property
    def get_config(self) -> dict:
        return {
            "host": self.__host,
            "port": self.__port,
            "user": self.__user,
            "password": self.__password,
            "db_name": self.__db_name
        }

