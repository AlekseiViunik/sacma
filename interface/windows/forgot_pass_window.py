from .base_window import BaseWindow
from PyQt6.QtWidgets import QDialog
# from handlers.json_handler import JsonHandler
# from logic.logger import logger as log
# from settings import settings as sett


class ForgotPasswordWindow(QDialog, BaseWindow):

    def __init__(
        self,
        window_name: str,
        file_path: str
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name

        self.init_ui()

    def remember_password(self) -> None:
        pass
