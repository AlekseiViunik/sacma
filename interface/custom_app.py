from PyQt6.QtWidgets import QWidget

from interface.windows.settings_window import SettingsWindow
from handlers.json_handler import JsonHandler
from interface.creator import Creator
from interface.helper import Helper

CONFIG_FILE = "windows_configs/main_window.json"


class CustomApp(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 0
        self.height = 0
        self.config_json_handler = JsonHandler(CONFIG_FILE)
        self.creator = None
        self.init_ui()

    def init_ui(self):
        # Загружаем конфиг
        config = self.config_json_handler.get_all_data()

        # Настраиваем окно
        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        Helper.move_window_to_center(self)

        # Создаем слои и виджеты через креатор
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def connect_callback(self, button, callback_name, params):
        if callback_name == "open_settings":
            button.clicked.connect(self.open_settings)
        else:
            pass
