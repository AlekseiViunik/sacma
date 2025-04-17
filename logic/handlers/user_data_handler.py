from logic.handlers.json_handler import JsonHandler
from interface.windows.messagebox import Messagebox
from settings import settings as sett


class UserDataHandler:
    """
    Обработчик событий, связанных с созданием нового пользователя.

    Methods
    -------
    - add_new_user_data(user_data)
        Метод добавления данных нового пользователя в файл.
    """

    def __init__(self) -> None:
        self.auth_json_handler: JsonHandler = (
            JsonHandler(sett.USER_MAIN_DATA_FILE, True)
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
        username = user_data.pop(sett.USERNAME)
        if user_data.get(sett.PASSWORD):
            user_data.pop(sett.PASSWORD)
        if user_data.get(sett.REPEAT_PASSWORD):
            user_data.pop(sett.REPEAT_PASSWORD)

        self.auth_json_handler.write_into_file(key=username, value=user_data)

    def change_user_data(
        self,
        username: str,
        field: str,
        new_value: str
    ) -> None:
        """
        Изменяет данные пользователя в файле.

        Parameters
        ----------
        - username: str
            Имя пользователя, данные которого нужно изменить.

        - field: str
            Поле, которое нужно изменить.

        - new_value: str
            Новое значение поля.
        """

        self.auth_json_handler.write_into_file(
            key=username,
            key2=field,
            value=new_value
        )

        Messagebox.show_messagebox(
            sett.CHANGE_USER_DATA_SUCCESS,
            sett.D_CHANGE_USER_DATA_SUCCESS.format(field, new_value),
            None,
            sett.TYPE_INFO,
            exec=True
        )
