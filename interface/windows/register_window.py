from PyQt6.QtWidgets import QLineEdit, QCheckBox

from handlers.input_data_handler import InputDataHandler
from handlers.json_handler import JsonHandler
from handlers.user_data_handler import UserDataHandler
from helpers.authenticator import Authenticator
from settings import settings as set
from logic.logger import logging as log
from .base_window import BaseWindow
from .messagebox import Messagebox


class RegisterWindow(BaseWindow):
    """
    Окно регистрации нового пользователя.

    Attributes
    ----------
    - auth_json_handler: JsonHandler
        Обработчик JSON файла авторизации.

    - auth_successful: bool
        Флаг успешной авторизации.

    - auth: Authenticator
        Помощник, отвечающий за авторизацию и создание юзеров.

    - input_data_handler: InputDataHandler
        Класс для обработки входных данных.

    - user_data_handler: UserDataHandler
        Класс для работы с данными юзера.

    Methods
    -------
    - create_user()
        Создание новго юзера.

    - toggle_password(checkbox, field)
        Сокрытие/раскрытие символов для ввода чувствительных данных.
    """

    CONFIG_FILE = set.REGISTER_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.auth_json_handler: JsonHandler = JsonHandler(set.AUTH_FILE)
        # TODO отдельный класс для создания нового юзера.
        self.auth: Authenticator = Authenticator()
        self.input_data_handler: InputDataHandler = InputDataHandler()
        self.user_data_handler: UserDataHandler = UserDataHandler()

        self.init_ui()

    def create_user(self) -> None:
        """
        Метод создания нового юзера. Под созданием подразумевается внесение его
        чувствительных данных в файл auth.json (Мы пока не используем БД) и
        обычных данных в user_main_data.json. Перед внесением данных проводятся
        проверки:
        - Все обязательные поля заполнены.
        - Юзернейм должен быть уникальным.
        - Пароль и его повторение должны совпадать.

        При успешном создании, создает информационное окно с соответствующей
        информацией.
        При невыполнении условий проверки создает окно об ошибке с
        соответствующим сообщением.
        """

        log.info("Button Create has been pressed")

        # Собираем все введенные и выбранные данные в один словарь.
        all_inputs = self.input_data_handler.collect_all_inputs(
            self.creator.input_fields,
            self.creator.chosen_fields
        )
        log.info(f"Fulfilled fields are: {all_inputs}")

        # Проверка, все ли обязательные поля заполнены.
        difference = self.input_data_handler.check_mandatory(
            all_inputs,
            self.creator.mandatory_fields
        )
        if difference:
            log.error("Check failed. Not all necessary fields were fulfilled")
            log.error(f"Missing fields are {difference}")
            if len(difference) == 1:
                err_msg = f"The field '{difference[0]}' is mandatory!"
            else:
                missing_fields = ', '.join(difference)
                err_msg = (
                    f"The following fields are mandatory: {missing_fields}!"
                )
            Messagebox.show_messagebox(
                "Creation failed",
                err_msg,
                self
            )
            return

        # Проверка, совпадает ли введенный пароль с повторенным.
        if all_inputs['password'] != all_inputs['repeat_password']:
            log.error("Check failed. Pass and its repeat are different")
            Messagebox.show_messagebox(
                "Creation failed",
                "Password and its repeat are not identical",
                self
            )
            return

        # Юзернейм вынесен в отдельную переменную для вставки его в строку
        username = all_inputs['username']

        # Вносим чувствительные данные в auth.json
        if not self.auth.register_user(
            all_inputs['username'],
            all_inputs['password']
        ):
            log.error("Creation failed. User is already exists")
            Messagebox.show_messagebox(
                "Creation failed",
                "User is already exists",
                self
            )
            return
        else:
            # Если чувствительные данные успешно сохранены, вносим обычные
            # данные.
            log.info(
                "Creation succesfull. Login-Pass pair has been added to the DB"
            )
            log.info("Trying to add user data")
            self.user_data_handler.add_new_user_data(all_inputs)
            Messagebox.show_messagebox(
                "Success!",
                f"User {username} is created!",
                self,
                "info"
            )
            self.close()

    def toggle_password(
        self,
        checkbox: QCheckBox,
        field: str = "password"
    ) -> None:
        """
        Делает вводимые чувствитильные данные видимыми/невидимыми в зависимости
        от чекбокса, который находится рядом с полем ввода.

        Parameters
        ----------
        - checkbox: QCheckBox
            Объект чекбокса, на основе которого меняется видимость поля.

        - field: str
            Имя поля, видимость которого меняется.
        """
        if checkbox.isChecked():
            log.info("Checkbox for password is marked as 'checked'")
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            log.info("Checkbox for password is marked as 'unchecked'")
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Password
            )
