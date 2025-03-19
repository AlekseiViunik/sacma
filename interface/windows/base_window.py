from PyQt6.QtWidgets import QWidget, QPushButton, QCheckBox
from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from logic.logger import logger as log


class BaseWindow(QWidget):
    """Базовое окно для всех окон приложения."""

    CONFIG_FILE = None  # Путь к конфигу должен задаваться в наследниках

    def __init__(self, file_path=None):
        super().__init__()
        self.window_width = 0
        self.window_height = 0
        # Инициализируем обработчик JSON
        self.config_json_handler = (
            JsonHandler(file_path) if file_path else
            JsonHandler(self.CONFIG_FILE)
        )
        self.creator = None

    def init_ui(self):
        """Создает интерфейс окна на основе JSON-конфига."""

        log.info(f"Creating window with config: {self.CONFIG_FILE}")

        # Загружаем конфиг
        config = self.config_json_handler.get_all_data()

        if config:
            log.info(f"Config loaded successfully: {config}")
        else:
            log.error("Couldn't get the data from the file!")
            return

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])

        Helper.move_window_to_top_left_corner(self)

        log.info("Using creator to generate UI layout")
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def connect_callback(
        self,
        widget: QPushButton | QCheckBox,
        callback_name: str,
        params: dict = {},
        parent=None
    ):

        match callback_name:
            case "create_user":
                widget.clicked.connect(parent.create_user)

            case "close_window":
                widget.clicked.connect(lambda: self.cancel(parent))

            case "toggle_password":
                widget.stateChanged.connect(
                    lambda: parent.toggle_password(widget)
                )
            case "toggle_repeat_password":
                widget.stateChanged.connect(
                    lambda: parent.toggle_password(widget, "repeat_password")
                )
            case "try_login":
                widget.clicked.connect(parent.try_login)

            case "handle_start_button":
                widget.clicked.connect(parent.handle_start_button)

            case "browse_file":
                target_input = params.get("target_input")
                widget.clicked.connect(
                    lambda: parent.browse_file(target_input)
                )
            case "save_settings":
                widget.clicked.connect(parent.save_settings)

    def cancel(self, parent):
        log.info("Cancel button has been pressed")
        parent.close()
