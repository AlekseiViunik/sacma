import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

from settings import settings as sett

load_dotenv()


class MailHandler:
    """
    Обработчик почты. Отвечает за отправку писем пользователю.

    Methods
    -------
    - send_mail(to, subject, msg)
        Отправляет электронное письмо.

    - generate_recover_pass_message(userdata, temp_pass)
        Генерирует сообщение для восстановления пароля.
    """

    def __init__(self):
        self.smtp_server = os.getenv(sett.SMTP_SERVER_KEY)
        self.smtp_port = int(os.getenv(sett.SMTP_PORT_KEY))
        self.email_address = os.getenv(sett.EMAIL_ADDRESS_KEY)
        self.email_password = os.getenv(sett.EMAIL_PASSWORD_KEY)

    def send_mail(self, to: str, subject: str, msg: str) -> None:
        """
        Отправляет электронное письмо.

        Parameters
        ----------
        - to: str
            Адрес электронной почты получателя.

        - subject: str
            Тема письма.

        - msg: str
            Текст сообщения.
        """

        msg = MIMEText(msg)
        msg[sett.SUBJECT] = subject
        msg[sett.FROM] = self.email_address
        msg[sett.TO] = to

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)

    def generate_recover_pass_message(
        self,
        userdata: str,
        temp_pass: str
    ) -> str:
        """
        Генерирует сообщение для восстановления пароля.

        Parameters
        ----------
        - userdata: dict
            Данные пользователя, которому отправляется сообщение.

        - temp_pass: str
            Временный пароль для восстановления доступа.

        Returns
        -------
        - _: str
            Сформированное сообщение для восстановления пароля.
        """

        name = userdata.get(
            sett.NAME, userdata.get(
                sett.SURNAME, sett.EMPTY_STRING
            )
        )
        greeting = sett.D_GREETING.format(name) if name else sett.GREETING
        return sett.RECOVER_MAIL_MESSAGE.format(greeting, temp_pass)
