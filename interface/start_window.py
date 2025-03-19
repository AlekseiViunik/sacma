from PyQt6.QtWidgets import QPushButton

from interface.windows.input_window import InputWindow
from interface.windows.register_window import RegisterWindow
from interface.windows.settings_window import SettingsWindow
from handlers.json_handler import JsonHandler
from settings import settings as set
from logic.logger import logger as log
from interface.windows.base_window import BaseWindow


class StartWindow(BaseWindow):

    CONFIG_FILE = set.MAIN_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0
        self.config_json_handler = JsonHandler(set.MAIN_WINDOW_CONFIG_FILE)
        self.creator = None
        self.init_ui()

    def open_settings(self) -> None:
        log.info("Settings button has been pressed!")
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def open_input_window(self, params) -> None:
        sender = self.sender()  # Получаем объект кнопки
        log.info(f"{sender.text()} button has been pressed!")
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна
            input_window = InputWindow(
                window_name,
                params['json_file_path'],
                self
            )
        input_window.show()

    def open_register(self):
        log.info("Create user button has been pressed!")
        self.register_window = RegisterWindow()
        self.register_window.show()

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict
    ) -> None:
        if callback_name == "open_settings":
            button.clicked.connect(self.open_settings)
        elif callback_name == "open_input_window":
            button.clicked.connect(lambda: self.open_input_window(params))
        elif callback_name == "open_register":
            button.clicked.connect(self.open_register)
        else:
            pass
