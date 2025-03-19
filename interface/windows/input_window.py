from PyQt6.QtWidgets import QPushButton

from handlers.input_data_handler import InputDataHandler
from helpers.remover import Remover
from interface.windows.output_window import OutputWindow
from logic.calculator import Calculator
from logic.logger import logger as log
from .base_window import BaseWindow


class InputWindow(BaseWindow):
    def __init__(
        self,
        window_name: str,
        file_path: str,
        parent_window
    ) -> None:
        super().__init__(file_path)
        self.window_name = window_name
        self.remover: Remover = Remover()
        self.parent_window = parent_window
        self.output_window: OutputWindow = None
        self.result: dict = None
        self.input_data_handler = InputDataHandler()

        self.init_ui()

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict = {},
        parent=None
    ) -> None:
        if callback_name == "handle_start_button":
            button.clicked.connect(self.handle_start_button)
        else:
            pass

    def handle_start_button(self):
        log.info("Button Invia has been pressed")
        all_inputs = self.input_data_handler.collect_all_inputs(
            self.creator.input_fields,
            self.creator.chosen_fields
        )
        calculator = Calculator(
            all_inputs,
            self.window_name,
            self.creator.current_changing_values
        )
        self.output_window = OutputWindow()
        log.info("Start calculating")
        result, post_message = calculator.calc_data()

        log.info("Open response widget")
        self.output_window.open_result_window(result, "Result", post_message)
