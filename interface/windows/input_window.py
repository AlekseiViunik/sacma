from PyQt6.QtWidgets import QWidget, QPushButton

from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from helpers.remover import Remover
from logic.calculator import Calculator


class InputWindow(QWidget):
    def __init__(
        self,
        window_name: str,
        file_path: str,
        parent_window
    ) -> None:
        super().__init__()
        self.window_name = window_name
        self.file_path = file_path
        self.config_json_handler = JsonHandler(self.file_path)
        self.creator: Creator | None = None
        self.remover: Remover = Remover()
        self.parent_window = parent_window

        self.init_ui()

    def init_ui(self):
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

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict = {}
    ) -> None:
        if callback_name == "handle_start_button":
            button.clicked.connect(self.handle_start_button)
        else:
            pass

    def handle_start_button(self):
        self.remover.clean_up_fields(
            self.creator.input_fields,
            self.creator.chosen_fields
        )
        all_inputs = {}
        for name, field in self.creator.chosen_fields.items():
            all_inputs[name] = field
        for name, field in self.creator.input_fields.items():
            all_inputs[name] = field
        calculator = Calculator(all_inputs)
        calculator.calc_data()
