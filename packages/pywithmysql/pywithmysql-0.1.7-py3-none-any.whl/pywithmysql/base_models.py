from pywithmysql.table import Table
from pywithmysql.config import DataBaseConfig
from pywithmysql.types import VarCharField
from pywithmysql.columns import Column
from pywithmysql.settings import SettingsTable
from pywithmysql.hash import hash_passwd
from pywithmysql.dataclassesmodels import RolesData, UserData


class UserModel:
    def __init__(self, config: DataBaseConfig, user: UserData):
        self.table = Table(
            "users",
            config,
            Column(name="username", type_=VarCharField, nullable=False, max_length=50, default=None, unique=True),
            Column(name="email", type_=VarCharField, nullable=False, max_length=100, default=None, unique=True),
            Column(name="password", type_=VarCharField, nullable=False, max_length=255, default=None, unique=False),
        )
        self.table_settings = SettingsTable(config, "users")
        self.user = user

    def create_user(self):
        try:
            self.table.create_table()
            self.table_settings.connect()
            self.table_settings.create(
                ["username", "email", "password", "created_at"],
                [f"'{self.user.username}'", f"'{self.user.email}'", f"'{hash_passwd(self.user.password)}'"]
            )
        except Exception:
            self.table_settings.connect()
            self.table_settings.create(
                ["username", "email", "password"],
                [f"'{self.user.username}'", f"'{self.user.email}'", f"'{hash_passwd(self.user.password)}'"]
            )


class RolesModel:
    def __init__(self, config: DataBaseConfig, role: RolesData):
        self.table = Table(
            "roles",
            config,
            Column(name="role_name", type_=VarCharField, nullable=False, max_length=50, unique=True),
        )
        self.table_settings = SettingsTable(config, "users")
        self.role = role

    def create_role(self):
        try:
            self.table.create_table()
            self.table_settings.connect()
            self.table_settings.create(
                ["role_name"],
                [f"'{self.role.role_name}'"]
            )
        except Exception:
            self.table_settings.connect()
            self.table_settings.create(
                ["role_name"],
                [f"'{self.role.role_name}'"]
            )


if __name__ == "__main__":
    config = DataBaseConfig(
        host="localhost",
        port=3306,
        user="root",
        password="29062008Kl!",
        db_name="test2"
    )

    user_data = UserData(username="user1", email="user1@example.com", password="password123")
    user_model = UserModel(config, user_data)
    user_model.table_settings.connect()
    print(user_model.table_settings.read_all())