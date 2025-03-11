import json
import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QHBoxLayout
)

SETTINGS_FILE = "settings.json"


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Настройки")
        self.setGeometry(200, 200, 350, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Путь к Excel файлу:")

        file_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.browse_button = QPushButton("Обзор")
        self.browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.input_field)
        file_layout.addWidget(self.browse_button)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_settings)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addLayout(file_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
                self.input_field.setText(settings.get("excel_path", ""))

    def save_settings(self):
        settings = {"excel_path": self.input_field.text()}
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        self.close()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать файл",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path:
            self.input_field.setText(file_path)
