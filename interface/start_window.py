from handlers.excel_handler import ExcelHandler
from handlers.json_handler import JsonHandler
from interface.windows.base_window import BaseWindow
from interface.windows.change_pass_window import ChangePassWindow
from interface.windows.delete_user_window import DeleteUserWindow
from interface.windows.input_window import InputWindow
from interface.windows.login_window import LoginWindow
from interface.windows.register_window import RegisterWindow
from interface.windows.settings_window import SettingsWindow
from logic.config_generator import ConfigGenerator
from logic.logger import logger as log
from settings import settings as sett


class StartWindow(BaseWindow):
    """
    Стартовое окно с кнопками открытия второстепенных окон.

    Attributes
    ----------
    - username: str
        Логин юзера, под которым выполнен вход.

    - excel_handler: ExcelHandler | None
        Обработчик Excel файла, который будет использоваться в дальнейшем.

    Methods
    -------
    - open_settings(target_input)
        Открывает окно пользовательских настроек.

    - open_input_window()
        Открывает выбранное окно ввода данных.

    - open_register()
        Открывает окно регистрации нового юзера.

    - logout()
        Закрывает текущее окно и открывает окно логина. Срабатывает при
        нажатии соответствующей кнопки.

    - change_password()
        Открывает окно смены пароля. Срабатывает при нажатии соответствующей
        кнопки.
    """

    CONFIG_FILE = sett.MAIN_WINDOW_CONFIG_FILE

    def __init__(
        self,
        username: str = sett.ALEX,
        excel_handler: ExcelHandler | None = None
    ) -> None:
        super().__init__(username=username)

        self.userdata = JsonHandler(
            sett.USER_MAIN_DATA_FILE, True
        ).get_value_by_key(self.username)

        self.excel_handler = excel_handler
        self.init_ui()

    def open_settings(self) -> None:
        """
        Открывает окно пользовательских настроек.
        """

        log.info(sett.SETTINGS_BUTTON_PRESSED)
        self.settings_window = SettingsWindow()
        if self.settings_window.exec():
            self.excel_handler.close_excel()
            self.excel_handler.open_excel()
            self.creator.update_dependent_layouts()

    def open_input_window(self, params: dict[str, str]) -> None:
        """
        Открывает выбранное окно ввода данных.

        Parameters
        ----------
        params: dict[str, str]
            Параметры для кнопки окна открытия. По сути содержат пока что
            только одно значение - путь к файлу с конфигом этого окна.
        """

        sender = self.sender()  # Получаем объект кнопки
        log.info(sett.BUTTON_PRESSED.format(sender.text()))
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна
            input_window = InputWindow(
                window_name,
                params[sett.JSON_FILE_PATH],
                self.excel_handler
            )

            # Для тестов
            self._last_input_window = input_window

        input_window.show()

    def open_register(self) -> None:
        """
        Открывает окно регистрации нового юзера.
        """

        log.info(sett.CREATE_USER_BUTTON_PRESSED)
        self.register_window = RegisterWindow()
        self.register_window.show()

    def logout(self) -> None:
        """
        Закрывает текущее окно и открывает окно логина.
        """
        self.hide()
        self.login_window = LoginWindow()
        if self.login_window.exec():
            self.username = self.login_window.username
            self.userdata = JsonHandler(
                sett.USER_MAIN_DATA_FILE, True
            ).get_value_by_key(self.username)
            self.show()
            default_config = self.config_json_handler.get_all_data()
            self._add_greetings_to_config(default_config)
            default_config = ConfigGenerator().add_logo_to_config(
                default_config, sett.MINUS_ONE
            )
            self.creator.config = default_config
            self.creator.update_dependent_layouts()

    def change_password(self) -> None:
        """
        Открывает окно смены пароля.
        """
        self.change_password_window = ChangePassWindow(self.username)
        self.change_password_window.show()

    def open_delete_user(self, params: dict[str, str]) -> None:
        """
        Открывает окно удаления юзера.
        """

        sender = self.sender()
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна

            delete_user_window = DeleteUserWindow(
                window_name,
                params[sett.JSON_FILE_PATH],
            )

            delete_user_window.show()
