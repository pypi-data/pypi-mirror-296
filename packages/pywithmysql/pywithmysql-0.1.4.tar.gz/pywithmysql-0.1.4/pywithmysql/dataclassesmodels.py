from dataclasses import dataclass


@dataclass
class UserData:
    username: str
    email: str
    password: str

class RolesData:
    role_name: str