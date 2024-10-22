from flask_login import UserMixin


class UserEntity(UserMixin):
    def __init__(self, id: int, name: str, nickname: str, password: str):
        self.id = id
        self.name = name
        self.nickname = nickname
        self.password = password

    def __str__(self):
        return f"UserEntity({self.id}, {self.name}, {self.nickname})"
