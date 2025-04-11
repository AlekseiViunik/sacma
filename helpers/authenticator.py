import hashlib
import os

from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as sett


class Authenticator:
    """
    Класс для управления авторизацией пользователей.

    Methods
    -------
    - load_users()
        Загружает чувствительные данные всех юзеров. Их немного - можем
        позволить.

    - load_last_user()
        Загружает последнего успешно вошедшего юзера (только username).

    - save_last_user(username)
        Сохраняет последнего успешно вошедшего юзера (только юзернейм).

    - register_user(username, password).
        Добавляет нового юзера (юзернейм и хешированный пароль)в файл
        аутентификации.

    - update_user_password(username, password)
        Обновляет пароль пользователя.

    - hash_password(password)
        Хеширует пароль.

    - verify_user(username, password)
        Проверяет соответствие логина паролю.

    """

    def __init__(self) -> None:
        self.file_handler: JsonHandler = JsonHandler(sett.AUTH_FILE, True)

    def load_users(self) -> dict:
        """
        Загружает всех пользователей из auth.json.

        Returns
        -------
        - _: dict
            Словарь с данными (логин + хешированный пароль) всех юзеров.
        """

        if not os.path.exists(sett.AUTH_FILE):
            return {sett.USERS: {}, sett.LAST_USER: sett.EMPTY_STRING}

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
        last_user = sett.EMPTY_STRING
        if last_user := self.file_handler.get_value_by_key(sett.LAST_USER):
            log.info(sett.LAST_USER_FOUND.format(last_user))
        return self.file_handler.get_value_by_key(sett.LAST_USER)

    def save_last_user(self, username: str) -> None:
        """
        Сохраняет последнего вошедшего пользователя, чтобы использовать его как
        юзернейм для следующего входа.

        Parameters
        ----------
        - username: str
            Логин
        """
        log.info(sett.SAVE_LAST_USER)
        self.file_handler.write_into_file(key=sett.LAST_USER, value=username)

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

        if username in users_data[sett.USERS]:
            return False  # Пользователь уже существует

        users_data[sett.USERS][username] = self.file_handler.write_into_file(
            sett.USERS,
            username,
            Authenticator().hash_password(password)
        )

        return True

    def update_user_password(username: str, password: str) -> bool:
        """
        Обновляет пароль пользователя.

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
        if username not in users_data[sett.USERS]:
            return False
        users_data[sett.USERS][username] = Authenticator().hash_password(
            password
        )
        Authenticator().file_handler.rewrite_file(users_data)
        user = Authenticator().load_users()[sett.USERS][username]
        return True if user else False

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с помощью SHA-256.

        Returns
        -------
        - _: str
            Хешированный пароль для записи хеша в файл.
        """
        log.info(sett.HASHING_PASS)
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
        log.info(sett.CHECK_USER_EXISTS.format(username, password))
        return users_data[sett.USERS].get(username) == hashed_password
