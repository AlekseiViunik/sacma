import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


class MailHandler:

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")

    def send_mail(self, to, subject, msg):
        msg = MIMEText(msg)
        msg["Subject"] = subject
        msg["From"] = self.email_address
        msg["To"] = to

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)

    def generate_recover_pass_message(self, userdata, temp_pass):
        name = userdata.get(
            "name", userdata.get(
                "surname", ""
            )
        )
        greeting = f"Здравствуйте, {name}!" if name else "Здравствуйте!"
        return f"""
        {greeting}

        Вы запросили восстановление пароля.

        Ваш временный пароль: {temp_pass}

        Пожалуйста, измените его сразу после входа в систему.

        Если это были не вы, то париться не очем. Злоумышленники не смогут
        ничего сделать, поскольку личных данных мы не храним, БД у нас нет,
        и вообще приложение не представляет серьезной ценности ни для кого
        особо, кроме нас.

        С уважением,
        Ваша команда.
        """
