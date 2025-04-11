from logic.filepath_generator import FilepathGenerator
from .base_window import BaseWindow
from handlers.json_handler import JsonHandler
from logic.logger import logger as log
from settings import settings as sett


class DeleteUserWindow(BaseWindow):
    """
    Класс для окна удаления пользователя.
    Удаляет пользователя из JSON файла с данными пользователей и
    из JSON файла с аутентификацией.

    Attributes
    ----------
    - window_name: str
        Имя окна, которое будет отображаться в заголовке.

    - file_path: str
        Путь к конфигу, который будет использоваться построения окна.
        Передается в родительский класс BaseWindow.

    Methods
    -------
    - delete_user()
        Удаляет пользователя из JSON файлов с данными пользователей и
        аутентификацией.

    Private Methods
    ---------------
    - __remove_yourself_from_dropdown()
        Удаляет себя из выпадающего списка выбора пользователя, чтобы случайно
        не вызвать ошибку, попытавшись удалить себя.
    """
    def __init__(
        self,
        window_name: str,
        file_path: str,
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name

        self.init_ui()
        self.__remove_yourself_from_dropdown()

    def delete_user(self) -> None:
        """
        Удаляет записи о выбранным пользователем из JSON файлов с данными
        пользователей и аутентификацией. Выбор происходит по username.
        Username выбранного пользователя хранится в объекте класса Creator,
        который является атрибутом класса-родителя BaseWindow.
        """

        auth_json_handler = JsonHandler(
            sett.AUTH_FILE, True
        )

        user_data_json_handler = JsonHandler(
            sett.USER_MAIN_DATA_FILE, True
        )

        try:
            username = self.creator.chosen_fields[sett.USERNAME].currentText()

            auth = auth_json_handler.get_all_data()
            userdata = user_data_json_handler.get_all_data()

            filepath = FilepathGenerator.generate_settings_filepath(
                sett.SETTINGS_FILE, username
            )

            userdata.pop(username, None)
            auth[sett.USERS].pop(username, None)

            auth_json_handler.rewrite_file(auth)
            user_data_json_handler.rewrite_file(userdata)

            self.creator.update_dependent_layouts()
            self.__remove_yourself_from_dropdown()

        except Exception as e:
            log.error(sett.DELETE_USER_ERROR.format(username, e))
            return

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __remove_yourself_from_dropdown(self) -> None:
        """
        Чтобы случайно не вызвать ошибку, попытавшись удалить самого себя,
        удаляет себя из списка доступных юзеров для удаления.
        """
        dropdown = self.creator.chosen_fields[sett.USERNAME]
        current_options = [
            dropdown.itemText(i) for i in range(dropdown.count())
        ]

        if self.username in current_options:
            current_options.remove(self.username)
        dropdown.clear()
        dropdown.addItems(current_options)
