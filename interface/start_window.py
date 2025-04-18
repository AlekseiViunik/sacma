from interface.windows.base_window import BaseWindow
from interface.windows.my_profile_window import MyProfile
from interface.windows.delete_user_window import DeleteUserWindow
from interface.windows.input_window import InputWindow
from interface.windows.login_window import LoginWindow
from interface.windows.register_window import RegisterWindow
from interface.windows.settings_window import SettingsWindow
from interface.windows.users_settings_window import UsersSettingsWindow
from logic.generators.config_generator import ConfigGenerator
from logic.generators.filepath_generator import FilepathGenerator
from logic.handlers.dropbox_handler import DropboxHandler
from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.json_handler import JsonHandler
from logic.logger import LogManager as lm
from settings import settings as sett


class StartWindow(BaseWindow):
    """
    Стартовое окно с кнопками открытия второстепенных окон.

    Attributes
    ----------
    - username: str
        Default = 'alex'\n
        Логин юзера, под которым выполнен вход.

    - excel_handler: ExcelHandler | None
        Defult = None\n
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

    - open_my_profile()
        Открывает окно настроек юзера. Срабатывает при нажатии соответствующей
        кнопки.
    """

    CONFIG_FILE = sett.MAIN_WINDOW_CONFIG_FILE

    def __init__(
        self,
        username: str = sett.ALEX,
        excel_handler: ExcelHandler | None = None,
        dropbox_handler: DropboxHandler | None = None,
        user_settings_path: str = sett.SETTINGS_FILE
    ) -> None:
        super().__init__(username=username)

        self.userdata = JsonHandler(
            sett.USER_MAIN_DATA_FILE, True
        ).get_value_by_key(self.username)

        self.excel_handler = excel_handler
        self.dropbox_handler = dropbox_handler
        self.user_settings_path = user_settings_path

        self.init_ui()

    def open_settings(self) -> None:
        """
        Открывает окно пользовательских настроек.
        """

        lm.log_info(sett.SETTINGS_BUTTON_PRESSED)

        lm.log_info(sett.CREATE_SETTINGS_WINDOW)
        self.settings_window = SettingsWindow(self.user_settings_path)

        if self.settings_window.exec():
            lm.log_info(sett.SETTINGS_WERE_CHANGED)
            self.dropbox_handler.restart_excel(
                self.user_settings_path
            )
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
        lm.log_info(sett.BUTTON_PRESSED, sender.text())

        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна

            lm.log_info(sett.CREATE_WINDOW, window_name)
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
        lm.log_info(sett.CREATE_USER_BUTTON_PRESSED)
        lm.log_info(sett.CREATE_REGISTER_WINDOW)
        self.register_window = RegisterWindow()
        self.register_window.show()

    def logout(self) -> None:
        """
        Закрывает текущее окно и открывает окно логина.
        """

        lm.log_info(sett.LOGOUT_BUTTON_PRESSED)
        lm.log_info(sett.HIDE_START_WINDOW)
        self.hide()

        lm.log_info(sett.CREATE_LOGIN_WINDOW)
        self.login_window = LoginWindow()
        if self.login_window.exec():
            lm.log_info(sett.SUCCESSFUL_LOGIN)
            lm.log_info(sett.SWITCHING_LOG_FILE)
            lm.switch_log_to_user(self.login_window.username)
            lm.log_info(sett.LOG_DELIMITER)

            self.username = self.login_window.username
            self.user_settings_path = (
                FilepathGenerator.generate_settings_filepath(
                    sett.SETTINGS_FILE, self.username
                )
            )
            lm.log_info(
                sett.NEW_USER_AND_SETTINGS_PATH_ARE,
                self.username,
                self.user_settings_path
            )

            self.userdata = JsonHandler(
                sett.USER_MAIN_DATA_FILE, True
            ).get_value_by_key(self.username)

            self.show()

            lm.log_info(sett.RERENDER_WINDOW)
            default_config = self.config_json_handler.get_all_data()
            self._add_greetings_to_config(default_config)
            default_config = ConfigGenerator().add_logo_to_config(
                default_config, sett.MINUS_ONE
            )
            self.creator.config = default_config
            self.dropbox_handler.restart_excel(
                self.user_settings_path
            )
            self.creator.update_dependent_layouts()

    def open_my_profile(self) -> None:
        """
        Открывает окно смены пароля.
        """
        lm.log_info(sett.MY_PROFILE_BUTTON_PRESSED)
        lm.log_info(sett.CREATE_MY_PROFILE_WINDOW)
        self.my_profile_window = MyProfile(self.username)
        self.my_profile_window.show()

    def open_delete_user(self, params: dict[str, str]) -> None:
        """
        Открывает окно удаления юзера.
        """

        sender = self.sender()
        lm.log_info(sett.BUTTON_PRESSED, sender.text())
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна

            lm.log_info(sett.CREATE_DELETE_USER_WINDOW)
            delete_user_window = DeleteUserWindow(
                window_name,
                params[sett.JSON_FILE_PATH],
                self.username
            )

            delete_user_window.show()

    def open_users_settings(self, params: dict[str, str]) -> None:
        """
        Открывает окно настроек юзера.
        """

        sender = self.sender()
        lm.log_info(sett.BUTTON_PRESSED, sender.text())
        if sender:
            window_name = sender.text()
            lm.log_info(sett.CREATE_USERS_SETTINGS_WINDOW)
            users_settings_window = UsersSettingsWindow(
                window_name,
                params[sett.JSON_FILE_PATH]
            )
            users_settings_window.show()
