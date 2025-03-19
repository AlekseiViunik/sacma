from PyQt6.QtWidgets import (
    QCheckBox, QPushButton, QMessageBox, QLineEdit
)

from handlers.json_handler import JsonHandler
from helpers.authenticator import Authenticator
from logic.logger import logging as log
from settings import settings as set
from .base_window import BaseWindow


class LoginWindow(BaseWindow):

    CONFIG_FILE = set.LOGIN_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.auth_json_handler = JsonHandler(set.AUTH_FILE)
        self.auth_successful: bool = False
        self.auth = Authenticator()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек.
        """
        super().init_ui()  # ✅ Вызываем базовый метод

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
