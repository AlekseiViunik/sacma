from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as set


class UserDataHandler:
    """
    Обработчик событий, связанных с созданием нового пользователя.

    Attributes
    ----------
    - auth_json_handler: JsonHandler
        Обработчик JSON файлов. Поскольку на текущий момент данные о юзерах
        хранятся в JSON файле, то нам будет нужен обработчик для работы с
        этим файлом для добавления туда новых юзеров и извлечения уже
        существующих при необходимости.

    Methods
    -------
    - add_new_user_data(user_data)
        Метод добавления данных нового пользователя в файл.
    """

    def __init__(self) -> None:
        self.auth_json_handler: JsonHandler = (
            JsonHandler(set.USER_MAIN_DATA_FILE)
        )

    def add_new_user_data(self, user_data: dict) -> None:
        """
        Добавляет в файл данные о новом пользователе, кроме чувствительных
        дынных, таких как пароль и его повторение.

        Parameters
        ----------
        - user_data: dict
            Данные юзера для добавления в файл.
        """

        # Убираем чувствительные данные из добавляемых
        # Также убираем оттуда юзернейм - он будет служить ключом, а не
        # значением в новом словаре.
        username = user_data.pop(set.USERNAME)
        if user_data.get(set.PASSWORD):
            user_data.pop(set.PASSWORD)
        if user_data.get(set.REPEAT_PASSWORD):
            user_data.pop(set.REPEAT_PASSWORD)

        log.info(set.TRYING_ADD_USER_DATA)
        log.info(f"The path is {set.USER_MAIN_DATA_FILE}")
        self.auth_json_handler.write_into_file(key=username, value=user_data)

        # Проверка, что пользователь добавлен (для логов)
        new_data = self.auth_json_handler.get_all_data()
        if new_data.get(username) and new_data[username] == user_data:
            log.info(set.USER_DATA_IS_ADDED)
        else:
            log.info(set.USER_DATA_IS_NOT_ADDED)
