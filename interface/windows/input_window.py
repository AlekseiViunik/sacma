from PyQt6.QtWidgets import QWidget, QPushButton

from handlers.input_data_handler import InputDataHandler
from handlers.json_handler import JsonHandler
from interface.creator import Creator

from helpers.helper import Helper
from helpers.remover import Remover
from interface.windows.output_window import OutputWindow
from logic.calculator import Calculator
from logic.logger import logger as log


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
        self.output_window: OutputWindow = None
        self.result: dict = None
        self.input_data_handler = InputDataHandler()

        self.init_ui()

    def init_ui(self):
        log.info(f"Create {self.window_name} window")
        log.info(f"Trying to get config data for {self.window_name} window")
        log.info(f"The path is {self.file_path}")
        config = self.config_json_handler.get_all_data()

        if config:
            log.info("Config data received")
            log.info(f"Config is: {config}")
        else:
            log.error("Couldn't get the data from the file!")

        # Настраиваем окно
        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        log.info(
            f"Use creator to place widgets on the {self.window_name} window"
        )
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
