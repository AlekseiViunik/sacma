import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

from interface.windows.settings_window import SettingsWindow
from handlers.json_handler import JsonHandler

CONFIG_FILE = "windows_configs/main_window.json"


class CustomApp(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 450
        self.height = 150
        self.config_json_handler = JsonHandler(CONFIG_FILE)
        self.creator = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Главное окно")
        self.setGeometry(100, 100, 400, 400)

        self.settings_button = QPushButton("Настройки", self)
        self.settings_button.setGeometry(150, 350, 100, 30)
        self.settings_button.clicked.connect(self.open_settings)

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CustomApp()
    main_window.show()
    sys.exit(app.exec())
