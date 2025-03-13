# import json
# import os

from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QFileDialog,
    QPushButton
)

from handlers.json_handler import JsonHandler
from interface.creator import Creator
from interface.helper import Helper

SETTINGS_FILE = "settings.json"
CONFIG_FILE = "windows_configs/settings_window.json"


class SettingsWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window_width = 0
        self.window_height = 0
        self.settings_json_handler = JsonHandler(SETTINGS_FILE)
        self.config_json_handler = JsonHandler(CONFIG_FILE)
        self.creator = None

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек.
        """
        config = self.config_json_handler.get_all_data()

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        Helper.move_window_to_center(self)

        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict
    ) -> None:
        """
        Привязывает коллбэки к кнопкам.
        """
        if callback_name == "close_window":
            button.clicked.connect(self.close)
        elif callback_name == "browse_file":
            target_input = params.get("target_input")
            button.clicked.connect(lambda: self.browse_file(target_input))
        elif callback_name == "save_settings":
            button.clicked.connect(self.save_settings)

    def browse_file(self, target_input: QLineEdit) -> None:
        """
        Метод, срабатывающий при нажатии кнопки Browse. Открывает окно выбора
        файла excel.
        """
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
        self.settings_json_handler.rewrite_file(
            self.creator.input_fields
        )
        self.close()
