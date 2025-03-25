import hashlib
import os

from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as set


class Authenticator:
    """
    Класс для управления авторизацией пользователей.

    Attributes
    ----------
    - file_handler: JsonHandler
        Обработчик JSON файла авторизации.

    Methods
    -------
    - load_users()
        Загружает чувствительные данные всех юзеров. Их немного - можем
        позволить.

    - load_last_user()
        Загружает последнего успешно вошедшего юзера (только username).

    - hash_password(password)
        Хеширует пароль.

    - verify_user(username, password)
        Проверяет соответствие логина паролю.

    - save_last_user(username)
        Сохраняет последнего успешно вошедшего юзера (только юзернейм).

    - register_user(username, password).
        Добавляет нового юзера (юзернейм и хешированный пароль)в файл
        аутентификации.
    """

    def __init__(self) -> None:
        self.file_handler: JsonHandler = JsonHandler(set.AUTH_FILE)

    def load_users(self) -> dict:
        """
        Загружает всех пользователей из auth.json.

        Returns
        -------
        - _: dict
            Словарь с данными (логин + хешированный пароль) всех юзеров.
        """

        if not os.path.exists(set.AUTH_FILE):
            return {set.USERS: {}, set.LAST_USER: set.EMPTY_STRING}

        return self.file_handler.get_all_data()

    def load_last_user(self) -> str:
        """
        Загружает последнего успешно вошедшего юзера (только юзернейм).

        Returns
        -------
        - _: str
            Юзернейм последнего успешно вошедшего юзера. Чтобы вставить его как
            дефолтное значение поля для ввода юзернейма.
        """
        last_user = set.EMPTY_STRING
        if last_user := self.file_handler.get_value_by_key(set.LAST_USER):
            log.info(f"Last user found {last_user}")
        return self.file_handler.get_value_by_key(set.LAST_USER)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с помощью SHA-256.

        Returns
        -------
        - _: str
            Хешированный пароль для записи хеша в файл.
        """
        log.info(set.HASHING_PASS)
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        """
        Проверяет логин и пароль пользователя.

        Parameters
        ----------
        - username: str
            Логин пользователя.

        - password: str
            Пароль пользователя.

        Returns
        -------
        - _: bool
            Информация об успешной/неуспешной авторизации.
        """
        users_data = Authenticator().load_users()
        hashed_password = Authenticator().hash_password(password)
        log.info(f"Check if the user {username} with pass '{password}' exists")
        return users_data[set.USERS].get(username) == hashed_password

    def save_last_user(self, username: str) -> None:
        """
        Сохраняет последнего вошедшего пользователя, чтобы использовать его как
        юзернейм для следующего входа.

        Parameters
        ----------
        - username: str
            Логин
        """
        log.info(set.SAVE_LAST_USER)
        self.file_handler.write_into_file(key=set.LAST_USER, value=username)

    def register_user(self, username: str, password: str) -> bool:
        """
        Записывает нового пользователя в auth.json, если валидация пройдена.

        Parameters
        ----------
        - username: str
            Логин

        - password: str
            Пароль

        Returns
        -------
        - _: bool
            Информация об успешной/неуспешной регистрации.
        """

        users_data = Authenticator().load_users()

        if username in users_data[set.USERS]:
            return False  # Пользователь уже существует

        users_data[set.USERS][username] = self.file_handler.write_into_file(
            set.USERS,
            username,
            Authenticator().hash_password(password)
        )

        return True
