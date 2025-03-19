from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QFileDialog,
    QPushButton
)

from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from settings import settings as set
from logic.logger import logger as log


class SettingsWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window_width = 0
        self.window_height = 0
        self.settings_json_handler = JsonHandler(set.SETTINGS_FILE)
        self.config_json_handler = JsonHandler(set.SETTINGS_WINDOW_CONFIG_FILE)
        self.creator = None

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек.
        """
        log.info("Create settings window")
        log.info("Trying to get config data for settings window")
        log.info(f"The path is {set.SETTINGS_WINDOW_CONFIG_FILE}")
        config = self.config_json_handler.get_all_data()

        if config:
            log.info("Config data received")
            log.info(f"Config is: {config}")
        else:
            log.error("Couldn't get the data from the file!")

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        Helper.move_window_to_center(self)

        log.info("Use creator to place widgets on the settings window")
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

    def connect_callback(
        self,
        button: QPushButton,
        callback_name: str,
        params: dict
    ) -> None:
        """
        Привязывает коллбэки к кнопкам.
        """
        if callback_name == "close_window":
            button.clicked.connect(self.cancel)
        elif callback_name == "browse_file":
            target_input = params.get("target_input")
            button.clicked.connect(lambda: self.browse_file(target_input))
        elif callback_name == "save_settings":
            button.clicked.connect(self.save_settings)

    def browse_file(self, target_input: QLineEdit) -> None:
        """
        Метод, срабатывающий при нажатии кнопки Browse. Открывает окно выбора
        файла excel.
        """
        log.info("Browse button has been pressed")
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Выбрать файл",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path and target_input in self.creator.input_fields:
            self.creator.input_fields[target_input].setText(file_path)
            self.creator.input_fields[target_input].setPlaceholderText(
                file_path
            )

    def save_settings(self) -> None:
        """
        Переписывает файл настроек и закрывает окно.
        """
        log.info("Save button has been pressed")
        log.info("Trying to rewrite settings file")
        log.info(f"The path is {set.SETTINGS_FILE}")
        log.info("Rewriting check is temporary unavailable")
        self.settings_json_handler.rewrite_file(
            self.creator.input_fields
        )
        self.close()

    def cancel(self):
        log.info("Cancel button has been pressed")
        self.close()
