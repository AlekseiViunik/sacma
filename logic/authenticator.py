import json
import hashlib
import os
from settings import settings as set


class Authenticator:
    """Класс для управления авторизацией пользователей."""

    @staticmethod
    def load_users():
        """Загружает пользователей из auth.json."""
        if not os.path.exists(set.AUTH_FILE):
            return {"users": {}, "lastUser": ""}

        with open(set.AUTH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширует пароль с помощью SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        """Проверяет логин и пароль пользователя."""
        users_data = Authenticator.load_users()
        hashed_password = Authenticator.hash_password(password)

        return users_data["users"].get(username) == hashed_password

    @staticmethod
    def save_last_user(username: str) -> None:
        """Сохраняет последнего вошедшего пользователя."""
        users_data = Authenticator.load_users()
        users_data["lastUser"] = username

        with open(set.AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4)

    @staticmethod
    def register_user(username: str, password: str) -> bool:
        """Регистрирует нового пользователя (если его нет)."""
        users_data = Authenticator.load_users()

        if username in users_data["users"]:
            return False  # Пользователь уже существует

        users_data["users"][username] = Authenticator.hash_password(password)

        with open(set.AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, indent=4)

        return True  # Успешно зарегистрирован
