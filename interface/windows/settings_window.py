from PyQt6.QtWidgets import (
    QLineEdit,
    QFileDialog
)

from handlers.json_handler import JsonHandler
from settings import settings as set
from logic.logger import logger as log
from .base_window import BaseWindow


class SettingsWindow(BaseWindow):

    CONFIG_FILE = set.SETTINGS_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.settings_json_handler = JsonHandler(set.SETTINGS_FILE)

        self.init_ui()

    def browse_file(self, target_input: QLineEdit) -> None:
        """
        Метод, срабатывающий при нажатии кнопки Browse. Открывает окно выбора
        файла excel.
        """
        log.info("Browse button has been pressed")
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Выбрать файл",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path and target_input in self.creator.input_fields:
            self.creator.input_fields[target_input].setText(file_path)
            self.creator.input_fields[target_input].setPlaceholderText(
                file_path
            )

    def save_settings(self) -> None:
        """
        Переписывает файл настроек и закрывает окно.
        """
        log.info("Save button has been pressed")
        log.info("Trying to rewrite settings file")
        log.info(f"The path is {set.SETTINGS_FILE}")
        log.info("Rewriting check is temporary unavailable")
        self.settings_json_handler.rewrite_file(
            self.creator.input_fields
        )
        self.close()
