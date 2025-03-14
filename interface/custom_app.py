from PyQt6.QtWidgets import QWidget, QPushButton

from interface.windows.input_window import InputWindow
from interface.windows.settings_window import SettingsWindow
from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper

CONFIG_FILE = "windows_configs/main_window.json"


class CustomApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.width = 0
        self.height = 0
        self.config_json_handler = JsonHandler(CONFIG_FILE)
        self.creator = None
        self.init_ui()

    def init_ui(self) -> None:
        # Загружаем конфиг
        config = self.config_json_handler.get_all_data()

        # Настраиваем окно
        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        # Создаем слои и виджеты через креатор
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def open_settings(self) -> None:
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def open_input_window(self, params) -> None:
        sender = self.sender()  # Получаем объект кнопки
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна
            input_window = InputWindow(
                window_name,
                params['json_file_path'],
                self
            )
        input_window.show()

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
        else:
            pass
