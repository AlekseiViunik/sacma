from PyQt6.QtWidgets import (
    QWidget, QPushButton
)

from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from helpers.authenticator import Authenticator
# from logic.logger import logging as log

AUTH_FILE = "auth.json"
CONFIG_FILE = "configs/windows_configs/register_window.json"


class RegisterWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window_width = 0
        self.window_height = 0
        self.auth_json_handler = JsonHandler(AUTH_FILE)
        self.config_json_handler = JsonHandler(CONFIG_FILE)
        self.auth_successful: bool = False
        self.creator = None
        self.auth = Authenticator()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек.
        """
        config = self.config_json_handler.get_all_data()

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict = {}
    ):
        if callback_name == "create_user":
            button.clicked.connect(self.create_user)

        elif callback_name == "close_window":
            button.clicked.connect(self.close)

    def create_user(self):
        pass
