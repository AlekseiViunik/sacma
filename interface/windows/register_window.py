from PyQt6.QtWidgets import QLineEdit, QCheckBox

from handlers.input_data_handler import InputDataHandler
from handlers.json_handler import JsonHandler
from handlers.user_data_handler import UserDataHandler
from helpers.authenticator import Authenticator
from settings import settings as sett
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

    CONFIG_FILE = sett.REGISTER_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.auth_json_handler: JsonHandler = JsonHandler(sett.AUTH_FILE)
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

        try:
            log.info(sett.CREATE_BUTTON_PRESSED)

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
                log.error(sett.MANDATORY_FIELDS_CHECK_FAILED)
                log.error(f"Missing fields are {difference}")
                if len(difference) == sett.SET_TO_ONE:
                    err_msg = f"The field '{difference[0]}' is mandatory!"
                else:
                    missing_fields = sett.LISTING_CONNECTOR.join(difference)
                    err_msg = (
                        "The following fields are mandatory: "
                        f"{missing_fields}!"
                    )
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    err_msg,
                    self
                )
                return

            # Проверка, совпадает ли введенный пароль с повторенным.
            if all_inputs[sett.PASSWORD] != all_inputs[sett.REPEAT_PASSWORD]:
                log.error(f"{sett.CHECK_FAILED} {sett.REPEAT_IS_DIFFERENT}")
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.REPEAT_IS_DIFFERENT,
                    self
                )
                return

            # Юзернейм вынесен в отдельную переменную для вставки его в строку
            username = all_inputs[sett.USERNAME]

            # Вносим чувствительные данные в auth.json
            if not self.auth.register_user(
                all_inputs[sett.USERNAME],
                all_inputs[sett.PASSWORD]
            ):
                log.error(f"{sett.CREATION_FAILED} {sett.USER_EXISTS}")
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.USER_EXISTS,
                    self
                )
                return
            else:
                # Если чувствительные данные успешно сохранены, вносим обычные
                # данные.
                log.info(
                    sett.AUTH_CREATION_SUCCESSFUL
                )
                log.info(sett.TRYING_ADD_AUTH_DATA)
                self.user_data_handler.add_new_user_data(all_inputs)
                Messagebox.show_messagebox(
                    sett.SUCCESS,
                    f"User {username} is created!",
                    self,
                    sett.TYPE_INFO
                )
                self.close()

        except Exception as e:
            log.error(f"Error caught: {e}")

    def toggle_password(
        self,
        checkbox: QCheckBox,
        field: str = sett.PASSWORD
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
            if field == sett.PASSWORD:
                log.info(sett.PASS_MARKED_AS_CHECKED)
            elif field == sett.REPEAT_PASSWORD:
                log.info(sett.PASS_REPEAT_MARKED_AS_CHECKED)
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            if field == sett.PASSWORD:
                log.info(sett.PASS_MARKED_AS_UNCHECKED)
            elif field == sett.REPEAT_PASSWORD:
                log.info(sett.PASS_REPEAT_MARKED_AS_UNCHECKED)
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Password
            )
