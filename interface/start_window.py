from typing import Dict
from interface.windows.input_window import InputWindow
from interface.windows.register_window import RegisterWindow
from interface.windows.settings_window import SettingsWindow
from settings import settings as set
from logic.logger import logger as log
from interface.windows.base_window import BaseWindow


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

    CONFIG_FILE = set.MAIN_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        # Своих атрибутов у класса нет.

        self.init_ui()

    def open_settings(self) -> None:
        """
        Открывает окно пользовательских настроек.
        """

        log.info("Settings button has been pressed!")
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def open_input_window(self, params: Dict[str, str]) -> None:
        """
        Открывает выбранное окно ввода данных.

        Parameters
        ----------
        params: Dict[str, str]
            Параметры для кнопки окна открытия. По сути содержат пока что
            только одно значение - путь к файлу с конфигом этого окна.
        """

        sender = self.sender()  # Получаем объект кнопки
        log.info(f"{sender.text()} button has been pressed!")
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна
            input_window = InputWindow(
                window_name,
                params['json_file_path']
            )
        input_window.show()

    def open_register(self) -> None:
        """
        Открывает окно регистрации нового юзера.
        """
        log.info("Create user button has been pressed!")
        self.register_window = RegisterWindow()
        self.register_window.show()
