from PyQt6.QtWidgets import QLineEdit, QCheckBox

from .base_window import BaseWindow
from .messagebox import Messagebox
from logic.handlers.input_data_handler import InputDataHandler
from logic.handlers.json_handler import JsonHandler
from logic.handlers.user_data_handler import UserDataHandler
from logic.helpers.authenticator import Authenticator
from logic.helpers.helper import Helper
from logic.helpers.validator import Validator
from logic.logger import LogManager as lm
from settings import settings as sett


class RegisterWindow(BaseWindow):
    """
    Окно регистрации нового пользователя.

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

            # Собираем все введенные и выбранные данные в один словарь.
            all_inputs = self.input_data_handler.collect_all_inputs(
                self.creator.input_fields,
                self.creator.chosen_fields
            )
            # Проверка, все ли обязательные поля заполнены.
            difference = self.input_data_handler.check_mandatory(
                all_inputs,
                self.creator.mandatory_fields
            )
            if difference:
                if len(difference) == sett.SET_TO_ONE:
                    err_msg = sett.MANDATORY_FIELD.format(
                        difference[sett.SET_TO_ZERO]
                    )
                else:
                    missing_fields = sett.LISTING_CONNECTOR.join(difference)
                    err_msg = (
                        sett.MANDATORY_FIELDS.format(missing_fields)
                    )
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    err_msg,
                    self
                )
                return

            # Проверка, совпадает ли введенный пароль с повторенным.
            if all_inputs[sett.PASSWORD] != all_inputs[sett.REPEAT_PASSWORD]:

                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.REPEAT_IS_DIFFERENT,
                    self
                )
                return

            if (
                sett.PRODUCTION_MODE_ON and
                not Validator.check_password_strength(
                    all_inputs[sett.PASSWORD]
                )
            ):
                lm.log_error(sett.PASSWORD_IS_WEAK)
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.PASSWORD_IS_WEAK,
                    self
                )
                return

            if (
                all_inputs[sett.EMAIL] != sett.EMPTY_STRING and
                not Validator.validate_email(
                    all_inputs[sett.EMAIL]
                )
            ):
                lm.log_error(sett.EMAIL_IS_NOT_VALID)
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.EMAIL_IS_NOT_VALID,
                    self
                )
                return

            if (
                all_inputs[sett.PHONE] != sett.EMPTY_STRING and
                not Validator.validate_phone(
                    all_inputs[sett.PHONE]
                )
            ):
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.PHONE_IS_NOT_VALID.format(all_inputs[sett.PHONE]),
                    self
                )
                return

            created_by = self.username
            created_on = Helper.get_current_time()

            all_inputs[sett.CREATED_BY] = created_by
            all_inputs[sett.CREATED_ON] = created_on

            # Юзернейм вынесен в отдельную переменную для вставки его в строку
            username = all_inputs[sett.USERNAME]

            # Вносим чувствительные данные в auth.json
            if not self.auth.register_user(
                all_inputs[sett.USERNAME],
                all_inputs[sett.PASSWORD]
            ):
                Messagebox.show_messagebox(
                    sett.CREATION_FAILED,
                    sett.USER_EXISTS,
                    self
                )
                return
            else:
                # Если чувствительные данные успешно сохранены, вносим обычные
                # данные.
                self.user_data_handler.add_new_user_data(all_inputs)
                Messagebox.show_messagebox(
                    sett.SUCCESS,
                    sett.USER_CREATED.format(username),
                    self,
                    sett.TYPE_INFO
                )
                self.close()

        except Exception as e:
            lm.log_exception(e)

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
            Default = 'password'\n
            Имя поля, видимость которого меняется.
        """

        if checkbox.isChecked():
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Normal
            )
        else:
            self.creator.input_fields[field].setEchoMode(
                QLineEdit.EchoMode.Password
            )
