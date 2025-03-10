import hashlib
import os

from logic.json_file_handler import JsonFileHandler
from settings import settings as set
from logic.logger import logger as log


class Authenticator:
    """Класс для управления авторизацией пользователей."""
    def __init__(self):
        self.file_handler = JsonFileHandler(set.AUTH_FILE)

    def load_users(self):
        """Загружает пользователей из auth.json."""
        if not os.path.exists(set.AUTH_FILE):
            return {"users": {}, "lastUser": ""}

        return self.file_handler.load_whole_file()

    def load_last_user(self) -> str:
        last_user = ""
        if last_user := self.file_handler.read_value_by_key("lastUser"):
            log.info(f"Last user found {last_user}")
        return self.file_handler.read_value_by_key("lastUser")

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширует пароль с помощью SHA-256."""
        log.info("Hashing the pass")
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        """Проверяет логин и пароль пользователя."""
        users_data = Authenticator().load_users()
        hashed_password = Authenticator().hash_password(password)
        log.info(f"Check if the user {username} with pass '{password}' exists")
        return users_data["users"].get(username) == hashed_password

    def save_last_user(self, username: str) -> None:
        """Сохраняет последнего вошедшего пользователя."""
        log.info("Save last user")
        self.file_handler.write_into_file(key="lastUser", value=username)

    def register_user(self, username: str, password: str) -> bool:
        """Регистрирует нового пользователя (если его нет)."""

        users_data = Authenticator().load_users()

        if username in users_data["users"]:
            return False  # Пользователь уже существует

        users_data["users"][username] = self.file_handler.write_into_file(
            "users",
            username,
            Authenticator().hash_password(password)
        )

        return True
