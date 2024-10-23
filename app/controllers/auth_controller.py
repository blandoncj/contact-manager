from dto.login_dto import LoginDTO
from entity.user import UserEntity
from dao.auth_dao import AuthDAO


class AuthController:
    def __init__(self):
        self.auth_dao = AuthDAO()

    def find_by_id(self, user_id: int) -> UserEntity:
        return self.auth_dao.find_by_id(user_id)

    def login(self, user: LoginDTO) -> UserEntity:
        return self.auth_dao.login(user)

    def register(self, user: UserEntity) -> None:
        self.auth_dao.register(user)
