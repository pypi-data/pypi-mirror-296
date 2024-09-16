class DataBaseConfig:
    def __init__(self,
                 host: str,
                 port: int,
                 password: str,
                 user: str,
                 db_name: str) -> None:
        self.__host = host
        self.__port = port
        self.__password = password
        self.__user = user
        self.__db_name = db_name

    @property
    def get_config(self) -> dict:
        return {
            "host": self.__host,
            "port": self.__port,
            "user": self.__user,
            "password": self.__password,
            "db_name": self.__db_name
        }

