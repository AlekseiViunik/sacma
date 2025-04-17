from PyQt6.QtWidgets import QDialog

from logic.helpers.helper import Helper

from .base_window import BaseWindow
from interface.windows.messagebox import Messagebox
from logic.handlers.mail_handler import MailHandler
from logic.helpers.authenticator import Authenticator
from logic.helpers.validator import Validator
from logic.handlers.json_handler import JsonHandler
from logic.generators.pass_generator import PassGenerator
from settings import settings as sett


class ForgotPasswordWindow(QDialog, BaseWindow):
    """
    Класс восстановления пароля.
    Позволяет пользователю восстановить пароль, отправив временный пароль на
    его электронную почту.

    Attributes
    ----------
    - window_name: str
        Имя окна, которое будет отображаться в заголовке.

    - file_path: str
        Путь к конфигу, который будет использоваться построения окна.
        Передается в родительский класс BaseWindow.

    Methods
    -------
    - recover_password()
        Восстанавливает пароль пользователя, отправляя временный пароль на его
        электронную почту.
    """
    def __init__(
        self,
        window_name: str,
        file_path: str
    ) -> None:
        super().__init__(file_path)
        self.window_name: str = window_name

        self.init_ui()

    def recover_password(self) -> None:
        """
        Восстанавливает пароль пользователя, отправляя временный пароль на его
        почту, если она есть. Но перед этим проводит валидацию введенных
        данных. Если данные не валидны, то выводит сообщение об ошибке.
        """

        username = self.creator.input_fields[sett.USERNAME].text()
        useremail = self.creator.input_fields[sett.EMAIL].text()
        if not Validator.validate_email(useremail):
            Messagebox.show_messagebox(
                sett.RECOVER_ERROR,
                sett.WRONG_EMAIL.format(useremail),
                None,
                exec=True
            )
            return

        userdata_json_handler = JsonHandler(sett.USER_MAIN_DATA_FILE, True)
        auth_json_handler = JsonHandler(sett.AUTH_FILE, True)

        userdata = userdata_json_handler.get_all_data()
        authdata = auth_json_handler.get_all_data()

        if (
            userdata.get(username) is None or
            authdata[sett.USERS].get(username) is None
        ):
            Messagebox.show_messagebox(
                    sett.RECOVER_ERROR,
                    sett.USER_NOT_FOUND,
                    None,
                    exec=True
                )
            return

        if (
            userdata[username].get(sett.EMAIL) is None or
            userdata[username].get(sett.EMAIL) == sett.EMPTY_STRING
        ):
            Messagebox.show_messagebox(
                    sett.RECOVER_ERROR,
                    sett.EMAIL_NOT_FOUND,
                    None,
                    exec=True
                )
            return

        if userdata[username][sett.EMAIL] != useremail:
            Messagebox.show_messagebox(
                    sett.RECOVER_ERROR,
                    sett.WRONG_CREDENTIALS,
                    None,
                    exec=True
                )
            return

        temp_pass = PassGenerator.generate_password(sett.SET_TO_TWENTY)
        hashed_temp_pass = Authenticator.hash_password(temp_pass)
        mailer = MailHandler()

        if sett.PRODUCTION_MODE_ON:
            try:
                mailer.send_mail(
                    useremail,
                    sett.RECOVER_PASS_SUBJECT,
                    mailer.generate_recover_pass_message(
                        userdata[username],
                        temp_pass
                    )
                )
            except Exception as e:
                Helper.log_exception(e)
                Messagebox.show_messagebox(
                    sett.RECOVER_ERROR,
                    sett.MAIL_ERROR.format(e),
                    None,
                    exec=True
                )
                return

        authdata[sett.USERS][username] = hashed_temp_pass
        auth_json_handler.rewrite_file(authdata)

        Messagebox.show_messagebox(
            sett.RECOVER_SUCCESS,
            sett.RECOVER_SUCCESS_MESSAGE,
            None,
            type=sett.TYPE_INFO,
            exec=True
        )
        self.close()
