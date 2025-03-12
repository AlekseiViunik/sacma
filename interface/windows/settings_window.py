# import json
# import os

from PyQt6.QtWidgets import (
    QWidget,
    # QFileDialog,
)

from handlers.json_handler import JsonHandler
from interface.creator import Creator
from interface.helper import Helper

SETTINGS_FILE = "settings.json"
CONFIG_FILE = "windows_configs/settings_window.json"


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 450
        self.height = 150
        self.settings_json_handler = JsonHandler(SETTINGS_FILE)
        self.config_json_handler = JsonHandler(CONFIG_FILE)

        self.init_ui()

    def init_ui(self):

        self.setWindowTitle("Настройки")
        Helper.move_window_to_center(self)

        config = self.config_json_handler.get_all_data()
        creator = Creator(config, self)
        layout = creator.create_window_layout()

        self.setLayout(layout)

    # def load_settings(self):
    #     if os.path.exists(SETTINGS_FILE):
    #         with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
    #             settings: json = json.load(f)
    #             self.input_excel_path.setText(settings.get("excel_path", ""))

    # def save_settings(self):
    #     settings = {"excel_path": self.input_excel_path.text()}
    #     with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
    #         json.dump(settings, f, indent=4)
    #     self.close()

    # def browse_file(self, filter, input):
    #     file_path, _ = QFileDialog.getOpenFileName(
    #         self,
    #         "Выбрать файл",
    #         "",
    #         filter
    #     )
    #     if file_path:
    #         input.setText(file_path)
