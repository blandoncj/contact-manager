class NicknameAlreadyExistsException(Exception):
    def __init__(self, nickname):
        self.nickname = nickname
        self.message = f"Nickname {nickname} already exists"
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    def __init__(self):
        self.message = "Username or password is incorrect"
        super().__init__(self.message)
