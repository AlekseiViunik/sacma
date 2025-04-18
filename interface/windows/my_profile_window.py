from PyQt6.QtWidgets import QLineEdit, QCheckBox

from logic.handlers.user_data_handler import UserDataHandler
from logic.helpers.authenticator import Authenticator
from logic.helpers.mover import Mover
from interface.windows.messagebox import Messagebox
from logic.helpers.validator import Validator
from logic.logger import LogManager as lm

from .base_window import BaseWindow
from settings import settings as sett


class MyProfile(BaseWindow):
    """
    Класс для окна смены пароля.

    Attributes
    ----------
    - username: str
        Имя пользователя, от которого открыто окно смены пароля.
        Передается в родительский класс BaseWindow.

    Methods
    -------
    - toggle_password(checkbox, field)
        Переключает режим отображения пароля в поле ввода.

    - change_pass()
        Сменяет пароль пользователя.
    """

    CONFIG_FILE = sett.MY_PROFILE_CONFIG_FILE

    def __init__(self, username: str) -> None:
        super().__init__(username=username)
        self.user_data_handler = UserDataHandler()
        self.init_ui()
        Mover.move_window_to_top_center(self)

    def toggle_password(
        self,
        checkbox: QCheckBox,
        field: str = sett.PASSWORD
    ) -> None:
        """
        Метод для переключения режима отображения пароля в поле ввода.
        Вызывается при активации/деактивации чекбокса "Показать пароль".

        Parameters
        ----------
        - checkbox: QCheckBox
            Чекбокс, который вызывает этот метод.
        - field: str
            Default = 'password'\n
            Поле ввода, для которого нужно переключить режим отображения
            пароля. По умолчанию - поле пароля.
        """

        if checkbox.isChecked():
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Password
            )

    def change_pass(self) -> None:
        """
        Метод для смены пароля. Вызывается при нажатии кнопки "Сменить
        пароль". В любом случае показывает окно с текстом об ошибке
        или успешной смене пароля.
        """

        lm.log_info(sett.TRYING_TO_CHANGE_PASS, self.username)
        old_pass = self.creator.input_fields[sett.OLD_PASSWORD].text()
        new_pass = self.creator.input_fields[sett.PASSWORD].text()
        repeat_pass = self.creator.input_fields[sett.REPEAT_PASSWORD].text()
        if (
            old_pass == sett.EMPTY_STRING or
            new_pass == sett.EMPTY_STRING or
            repeat_pass == sett.EMPTY_STRING
        ):
            lm.log_error(sett.EMPTY_FIELDS_ERROR)
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.EMPTY_FIELDS_ERROR,
                self
            )
            return

        if not Authenticator.verify_user(self.username, old_pass):
            lm.log_error(sett.WRONG_CREDENTIALS)
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.WRONG_OLD_PATH,
                self
            )
            return

        if new_pass != repeat_pass:
            lm.log_error(sett.REPEAT_IS_DIFFERENT)
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.REPEAT_IS_DIFFERENT,
                self
            )
            return

        if not Validator.check_password_strength(new_pass):
            lm.log_error(sett.PASSWORD_IS_WEAK)
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_ERROR,
                sett.PASSWORD_IS_WEAK,
                self
            )
            return

        if Authenticator.update_user_password(
            self.username,
            new_pass
        ):
            lm.log_info(sett.CHANGE_PASS_SUCCESS)
            Messagebox.show_messagebox(
                sett.CHANGE_PASS_SUCCESS,
                sett.CHANGE_PASS_SUCCESS,
                self,
                sett.TYPE_INFO
            )
            self.close()
        else:
            lm.log_error(sett.USER_NOT_FOUND)
            Messagebox.show_messagebox(
                sett.USER_NOT_FOUND,
                sett.USER_NOT_FOUND,
                self
            )

    def change_email(self) -> None:

        lm.log_info(sett.TRYING_TO_CHANGE_EMAIL, self.username)

        if not Validator.validate_email(
            self.creator.input_fields[sett.NEW_EMAIL].text()
        ):
            lm.log_error(sett.EMAIL_IS_NOT_VALID)
            Messagebox.show_messagebox(
                sett.CHANGING_FAILED,
                sett.EMAIL_IS_NOT_VALID,
                None,
                exec=True
            )
            return

        self.user_data_handler.change_user_data(
            username=self.username,
            field=sett.EMAIL,
            new_value=self.creator.input_fields[sett.NEW_EMAIL].text()
        )
        lm.log_info(sett.SUCCESS)

    def change_name(self) -> None:
        lm.log_info(sett.TRYING_TO_CHANGE_NAME, self.username)
        self.user_data_handler.change_user_data(
            username=self.username,
            field=sett.NAME,
            new_value=self.creator.input_fields[sett.NEW_NAME].text()
        )

    def change_surname(self) -> None:
        lm.log_info(sett.TRYING_TO_CHANGE_SURNAME, self.username)
        self.user_data_handler.change_user_data(
            username=self.username,
            field=sett.SURNAME,
            new_value=self.creator.input_fields[sett.NEW_SURNAME].text()
        )

    def change_phone(self) -> None:
        lm.log_info(sett.TRYING_TO_CHANGE_PHONE, self.username)
        if not Validator.validate_phone(
            self.creator.input_fields[sett.NEW_PHONE].text()
        ):
            lm.log_error(sett.PHONE_IS_NOT_VALID)
            Messagebox.show_messagebox(
                sett.CHANGING_FAILED,
                sett.PHONE_IS_NOT_VALID.format(
                    self.creator.input_fields[sett.NEW_PHONE].text()
                ),
                None,
                exec=True
            )
            return

        self.user_data_handler.change_user_data(
            username=self.username,
            field=sett.PHONE,
            new_value=self.creator.input_fields[sett.NEW_PHONE].text()
        )
        lm.log_info(sett.SUCCESS)

    def change_sex(self) -> None:
        lm.log_info(sett.TRYING_TO_CHANGE_SEX, self.username)
        self.user_data_handler.change_user_data(
            username=self.username,
            field=sett.SEX,
            new_value=self.creator.chosen_fields[sett.NEW_SEX].currentText()
        )
