from PyQt6.QtWidgets import QDialog

from .base_window import BaseWindow
from logic.handlers.json_handler import JsonHandler
from logic.logger import LogManager as lm
from settings import settings as sett


class SettingsWindow(QDialog, BaseWindow):
    """
    Окно настроек.

    Methods
    -------

    - save_settings()
        Переписывает файл настроек и закрывает окно.
    """

    CONFIG_FILE = sett.SETTINGS_WINDOW_CONFIG_FILE

    def __init__(self, user_settings_path: str = sett.SETTINGS_FILE) -> None:
        super().__init__()
        self.settings_json_handler = JsonHandler(user_settings_path, True)

        self.init_ui()

    def save_settings(self) -> None:
        """
        Переписывает файл настроек и закрывает окно.
        """

        try:
            input_data = self.creator.input_fields[sett.EXCEL_LINK].text()
            self.settings_json_handler.write_into_file(
                key=sett.EXCEL_LINK,
                value=input_data
            )
            self.accept()

        except Exception as e:
            lm.log_exception(e)
