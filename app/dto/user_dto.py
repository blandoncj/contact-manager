class UserDTO:
    def __init__(self, name: str, nickname: str, password: str):
        self.name = name
        self.nickname = nickname
        self.password = password

    def __str__(self):
        return f"UserDTO(name={self.name}, nickname={self.nickname}, password={self.password})"
