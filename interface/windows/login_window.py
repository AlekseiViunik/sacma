from PyQt6.QtWidgets import QLineEdit, QCheckBox

from handlers.json_handler import JsonHandler
from helpers.authenticator import Authenticator
from logic.logger import logging as log
from settings import settings as set
from .base_window import BaseWindow
from .messagebox import Messagebox


class LoginWindow(BaseWindow):
    """
    Класс, отвечающий за вывод окна авторизации.

    Attributes
    ----------
    - auth_json_handler: JsonHandler
        Обработчик файла JSON, содержащего логин и хешированный пароль.
    - auth_successful: bool
        Флаг успешности авторизации.
    - auth: Authenticator
        Хелпер для работы с авторизацией.

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
    """

    CONFIG_FILE = set.LOGIN_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.auth_json_handler: JsonHandler = JsonHandler(set.AUTH_FILE)
        self.auth_successful: bool = False
        self.auth: Authenticator = Authenticator()

        self.init_ui()

    def init_ui(self) -> None:
        """
        Создает интерфейс окна настроек. Повторяет весь функционал родителя,
        но также еще и заполняет поле Username, если были в auth.json есть поле
        lastUser.
        """
        super().init_ui()  # ✅ Вызываем базовый метод

        log.info(set.ADD_LAST_USER_TO_INPUT_FIELD)
        last_user = self.auth_json_handler.get_value_by_key(set.LAST_USER)
        if set.USERNAME in self.creator.input_fields:
            self.creator.input_fields[set.USERNAME].setText(last_user)

    def try_login(self) -> None:
        """
        Обрабатывает нажатие кнопки Prova/Try. В случае успешного входа,
        закрывает окно логина и открывает стартовое окно. В противном
        случае открывает Окно с информации о неверных логине и пароле.
        """
        log.info(set.TRY_BUTTON_PRESSED)
        username = self.creator.input_fields[set.USERNAME].text()
        password = self.creator.input_fields[set.PASSWORD].text()
        try:
            if self.auth.verify_user(username, password):
                log.info(set.USER_VERIFIED)
                self.auth.save_last_user(username)
                self.auth_successful = True
                self.close()  # Закрываем окно авторизации
            else:
                log.error(set.WRONG_CREDENTIALS)
                Messagebox.show_messagebox(
                    set.LOGIN_ERROR,
                    set.WRONG_CREDENTIALS,
                    self
                )
        except Exception as e:
            log.error(f"Error caught: {e}")

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
            log.info(set.PASS_MARKED_AS_CHECKED)
            self.creator.input_fields[set.PASSWORD].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            log.info(set.PASS_MARKED_AS_UNCHECKED)
            self.creator.input_fields[set.PASSWORD].setEchoMode(
                QLineEdit.EchoMode.Password
            )
