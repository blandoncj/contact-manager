from dto.login_dto import LoginDTO
from dto.user_dto import UserDTO
from entity.user import UserEntity
from dao.auth_dao import AuthDAO


class AuthController:
    def __init__(self):
        self.auth_dao = AuthDAO()

    def find_by_id(self, user_id: int) -> UserDTO:
        return self.auth_dao.find_by_id(user_id)

    def login(self, user: LoginDTO) -> UserDTO:
        return self.auth_dao.login(user)

    def register(self, user: UserEntity):
        self.auth_dao.register(user)
