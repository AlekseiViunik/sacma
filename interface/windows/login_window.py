from PyQt6.QtWidgets import QLineEdit, QCheckBox, QDialog

from .base_window import BaseWindow
from .messagebox import Messagebox
from interface.windows.forgot_pass_window import ForgotPasswordWindow
from logic.handlers.json_handler import JsonHandler
from logic.helpers.authenticator import Authenticator
from logic.logger import LogManager as lm
from settings import settings as sett


class LoginWindow(QDialog, BaseWindow):
    """
    Класс, отвечающий за вывод окна авторизации (логина).

    Methods
    -------
    - init_ui()
        Немного усовершенствованный метод родителя. Повторяет весь его
        функционал плюс реализует немного своего.

    - try_login()
        Метод обработки попытки ввода логина и пароля.

    - toggle_password(checkbox)
        Метод делающий ввода пароля видимым/невидимым в зависимости от
        Чекбокса.

    - forgot_password(params)
        Метод, открывающий окно восстановления пароля.
    """

    CONFIG_FILE = sett.LOGIN_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.username: str = sett.EMPTY_STRING
        self.auth_json_handler: JsonHandler = JsonHandler(sett.AUTH_FILE, True)
        self.auth_successful: bool = False
        self.auth: Authenticator = Authenticator()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек. Повторяет весь функционал родителя,
        но также еще и заполняет поле Username, если в auth.json есть поле
        lastUser.
        """

        super().init_ui()  # ✅ Вызываем базовый метод

        last_user = self.auth_json_handler.get_value_by_key(sett.LAST_USER)
        if sett.USERNAME in self.creator.input_fields:
            self.creator.input_fields[sett.USERNAME].setText(last_user)

    def try_login(self) -> None:
        """
        Обрабатывает нажатие кнопки Prova/Try. В случае успешного входа,
        закрывает окно логина и открывает стартовое окно. В противном
        случае открывает Окно с информации о неверных логине и пароле.
        """

        username = self.creator.input_fields[sett.USERNAME].text()
        password = self.creator.input_fields[sett.PASSWORD].text()
        lm.log_info(sett.TRYING_TO_LOGIN, username)
        try:
            if self.auth.verify_user(username, password):
                self.auth.save_last_user(username)
                self.username = username
                self.auth_successful = True
                lm.log_info(sett.SUCCESS)
                self.accept()
            else:
                lm.log_error(sett.WRONG_CREDENTIALS)
                Messagebox.show_messagebox(
                    sett.LOGIN_ERROR,
                    sett.WRONG_CREDENTIALS,
                    self
                )
        except Exception as e:
            lm.log_exception(e)

    def toggle_password(self, checkbox: QCheckBox) -> None:
        """
        Маскирует/снимает маскировку с символов, вводимых в поле password в
        зависимости от того, активирован ли чекбокс рядом с полем или нет.

        Parameters
        ----------
        - checkbox: QCheckBox
            Чекбокс, в зависимости от которого меняется наличие маскировки
            символов.
        """

        if checkbox.isChecked():
            self.creator.input_fields[sett.PASSWORD].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.creator.input_fields[sett.PASSWORD].setEchoMode(
                QLineEdit.EchoMode.Password
            )

    def forgot_password(self, params: dict) -> None:
        """
        Открывает окно восстановления пароля.

        Parameters
        ----------
        - params: dict
            Параметры для кнопки окна открытия. По сути содержат пока что
            только одно значение - путь к файлу с конфигом этого окна.
        """

        sender = self.sender()
        if sender:
            window_name = sender.text()  # Берем текст кнопки как имя окна

            self.forgot_pass_window = ForgotPasswordWindow(
                window_name,
                params[sett.JSON_FILE_PATH],
            )

            self.forgot_pass_window.setModal(True)
            self.forgot_pass_window.show()
