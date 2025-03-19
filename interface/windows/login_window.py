from PyQt6.QtWidgets import (
    QCheckBox, QWidget, QPushButton, QMessageBox, QLineEdit
)

from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from helpers.authenticator import Authenticator
from logic.logger import logging as log
from settings import settings as set


class LoginWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.window_width = 0
        self.window_height = 0
        self.auth_json_handler = JsonHandler(set.AUTH_FILE)
        self.config_json_handler = JsonHandler(set.LOGIN_WINDOW_CONFIG_FILE)
        self.auth_successful: bool = False
        self.creator = None
        self.auth = Authenticator()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек.
        """
        log.info("Create settings window")
        log.info("Trying to get config data for settings window")
        log.info(f"The path is {set.LOGIN_WINDOW_CONFIG_FILE}")
        config = self.config_json_handler.get_all_data()

        if config:
            log.info("Config data received")
            log.info(f"Config is: {config}")
        else:
            log.error("Couldn't get the data from the file!")

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        log.info("Use creator to place widgets on the settings window")
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

        log.info("Add last user to input field default value")
        last_user = self.auth_json_handler.get_value_by_key('lastUser')
        if "username" in self.creator.input_fields:
            self.creator.input_fields["username"].setText(last_user)

    def connect_callback(
        self,
        widget: QPushButton | QCheckBox,
        callback_name: str,
        params: dict = {}
    ):
        if isinstance(widget, QPushButton):
            if callback_name == "try_login":
                widget.clicked.connect(self.try_login)
            elif callback_name == "close_window":
                widget.clicked.connect(self.cancel)
        if isinstance(widget, QCheckBox):
            if callback_name == "toggle_password":
                widget.stateChanged.connect(
                    lambda: self.toggle_password(widget)
                )

    def try_login(self):
        log.info("Try button is pressed")
        username = self.creator.input_fields['username'].text()
        password = self.creator.input_fields['password'].text()
        if self.auth.verify_user(username, password):
            log.info("User verified")
            self.auth.save_last_user(username)
            self.auth_successful = True
            self.close()  # Закрываем окно авторизации
        else:
            log.error("Credentials are wrong")
            msg = QMessageBox(self)
            msg.setWindowTitle("Login error")
            msg.setText("Creadentials are wrong!")
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.show()

    def toggle_password(self, checkbox):
        if checkbox.isChecked():
            log.info("Checkbox for password is marked as 'checked'")
            self.creator.input_fields['password'].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            log.info("Checkbox for password is marked as 'unchecked'")
            self.creator.input_fields['password'].setEchoMode(
                QLineEdit.EchoMode.Password
            )

    def cancel(self):
        log.info("Cancel button is pressed")
        self.close()
