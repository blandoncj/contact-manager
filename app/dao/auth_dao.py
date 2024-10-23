import bcrypt
import sqlite3 as sql
from db.db_connection import DatabaseConnection
from dto.login_dto import LoginDTO
from entity.user import UserEntity
from exception.user_exceptions import (
    InvalidCredentialsException,
    NicknameAlreadyExistsException,
)


class AuthDAO:

    def find_by_id(self, user_id: int) -> UserEntity:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                result = cursor.fetchone()
                return (
                    UserEntity(result[0], result[1], result[2], result[3])
                    if result
                    else None
                )
        except sql.Error as e:
            print(f"Error on find_by_id: {e}")
            return None

    def isNicknameAvailable(self, nickname: str) -> bool:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM users WHERE nickname = ?", (nickname,)
                )
                count = cursor.fetchone()[0]
                return count == 0
        except sql.Error as e:
            print(f"Error on isNicknameAvailable: {e}")
            return False

    def register(self, user: UserEntity):
        if self.isNicknameAvailable(user.nickname):
            try:
                hashed_password = bcrypt.hashpw(
                    user.password.encode("utf-8"), bcrypt.gensalt()
                )
                with DatabaseConnection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO users (name, nickname, password) VALUES (?, ?, ?)",
                        (user.name, user.nickname, hashed_password),
                    )
                    conn.commit()
            except sql.Error as e:
                print(f"Error on register: {e}")
        else:
            raise NicknameAlreadyExistsException(user.nickname)

    def login(self, user: LoginDTO):
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT password FROM users WHERE nickname = ?", (user.nickname,)
                )

                hashed_password = cursor.fetchone()

                if hashed_password and bcrypt.checkpw(
                    user.password.encode("utf-8"), hashed_password[0]
                ):
                    cursor.execute(
                        "SELECT * FROM users WHERE nickname = ?", (user.nickname,)
                    )
                    result = cursor.fetchone()

                    if result:
                        return UserEntity(result[0], result[1], result[2], result[3])
                    else:
                        raise InvalidCredentialsException()
                else:
                    raise InvalidCredentialsException()
        except sql.Error as e:
            print(f"Error on login: {e}")
            return None
