from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from handlers.json_handler import JsonHandler
from helpers.helper import Helper
from logic.translator import Translator


FILE_PATH = "configs/windows_configs/output_window.json"


class OutputWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.config_json_handler = JsonHandler(FILE_PATH)

    def open_result_window(
        self,
        values,
        pre_message=None,
        post_message=None,
        only_keys=["price", "weight"]
    ):

        config = self.config_json_handler.get_all_data()

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаём шрифт (увеличенный размер)
        font = QFont()
        font.setPointSize(16)  # Размер шрифта

        if pre_message:
            pre_message_label = QLabel(pre_message)
            pre_message_label.setFont(font)
            pre_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(pre_message_label)

        grid_layout = QGridLayout()
        filtered_values = {k: v for k, v in values.items() if k in only_keys}
        filtered_values = Translator.translate_dict(filtered_values)
        row = 0
        for label, value in filtered_values.items():
            if label == "Prezzo" and value:
                value = f"{str(value)} €"
            elif label == "Peso" and value:
                value = f"{str(value)} Kg"

            label = f"{label}: "

            title_label = QLabel(label)
            value_label = QLabel(str(value))

            title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            title_label.setFont(font)
            value_label.setFont(font)

            grid_layout.addWidget(title_label, row, 0)
            grid_layout.addWidget(value_label, row, 1)
            row += 1

        main_layout.addLayout(grid_layout)

        if (post_message):
            post_message_label = QLabel(post_message)
            post_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            post_message_label.setFont(font)
            main_layout.addWidget(post_message_label)

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(100)
        ok_button.setFixedHeight(50)
        ok_button.setStyleSheet("margin-top: 10px;")
        ok_button.clicked.connect(self.close)
        button_container = QVBoxLayout()
        button_container.addWidget(
            ok_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        main_layout.addLayout(button_container)

        self.setLayout(main_layout)
        self.show()
