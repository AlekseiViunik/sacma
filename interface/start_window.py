from handlers.json_handler import JsonHandler
from interface.windows.base_window import BaseWindow
from interface.windows.input_window import InputWindow
from interface.windows.register_window import RegisterWindow
from interface.windows.settings_window import SettingsWindow
from logic.logger import logger as log
from settings import settings as sett


class StartWindow(BaseWindow):
    """
    Стартовое окно с кнопками открытия второстепенных окон.
    Своих атрибутов нет.

    Methods
    -------
    - open_settings(target_input)
        Открывает окно пользовательских настроек.

    - open_input_window()
        Открывает выбранное окно ввода данных.

    - open_register()
        Открывает окно регистрации нового юзера.
    """

    CONFIG_FILE = sett.MAIN_WINDOW_CONFIG_FILE

    def __init__(self, username: str = sett.EMPTY_STRING) -> None:
        super().__init__(username=username)
        # Своих атрибутов у класса нет.
        self.userdata = JsonHandler(sett.USER_MAIN_DATA_FILE).get_value_by_key(
            self.username
        )
        self.init_ui()

    def open_settings(self) -> None:
        """
        Открывает окно пользовательских настроек.
        """

        log.info(sett.SETTINGS_BUTTON_PRESSED)
        self.settings_window = SettingsWindow()
        self.settings_window.show()

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
                params[sett.JSON_FILE_PATH]
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
