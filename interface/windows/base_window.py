from datetime import datetime
from PyQt6.QtWidgets import QWidget, QPushButton, QCheckBox
from typing import Any

from interface.creators.creator import Creator
from logic.generators.config_generator import ConfigGenerator
from logic.handlers.json_handler import JsonHandler
from logic.helpers.mover import Mover
from logic.logger import LogManager as lm
from settings import settings as sett


class BaseWindow(QWidget):
    """
    Базовое окно для всех окон приложения.

    Attributes
    ----------
    - file_path: str | None
        Default = None\n
        Путь к файлу конфигурации. Если None, то используется путь из
        наследников.

    - username: str
        Default = 'alex'\n
        Имя пользователя, с которым открыто окно.

    Methods
    -------
    - init_ui()
        Метод отрисовки интерфейса окна. Использует Креатор.

    - connect_callback(widget, callback_name, params, inheritor)
        Привязывает методы наследников (или свои) к кнопкам по их конфигу.

    - cancel(inheritor)
        Свой метод для кнопки Cancel. Закрывает окно и пишет об этом в лог.

    Protected Methods
    -----------------
    - _add_greetings_to_config(config)
        Добавляет в конфиг приветствие для пользователя.
    """

    CONFIG_FILE = None  # Путь к конфигу должен задаваться в наследниках

    def __init__(
        self,
        file_path: str | None = None,
        username: str = sett.ALEX,
    ) -> None:
        super().__init__()
        self.username: str = username
        self.window_width: int = sett.SET_TO_ZERO
        self.window_height: int = sett.SET_TO_ZERO
        self.userdata: dict = {}

        # Для наследников, у которых путь к конфигу определяется динамически,
        # передаем file_path
        self.config_json_handler: JsonHandler = (
            JsonHandler(file_path) if file_path else
            JsonHandler(self.CONFIG_FILE)
        )
        self.creator: Creator | None = None

    def init_ui(self) -> None:
        """
        Создает интерфейс окна на основе JSON-конфига.
        - Загружает конфиг из JSON файла.
        - Добавляет лого в конфиг.
        - Добавляет приветствие в конфиг.
        - Настраивает Титул и размеры окна.
        - Перемещает окно в центр экрана.
        - Размещает виджеты, используя креатор.
        - Блокирует размеры окна, если это указано в конфиге.
        """

        lm.log_info(sett.LOAD_CONFIG_GUI)
        # Загружаем конфиг
        config = self.config_json_handler.get_all_data()

        if config.get(sett.WINDOW_TITLE) == sett.SACMA:
            lm.log_info(sett.ADD_GREETINGS_TO_CONFIG)
            config = self._add_greetings_to_config(config)

        lm.log_info(sett.ADD_LOGO_TO_CONFIG)
        config = ConfigGenerator().add_logo_to_config(config, sett.MINUS_ONE)

        self.setWindowTitle(config[sett.WINDOW_TITLE])
        self.window_width = int(config[sett.WINDOW_WIDTH])
        self.window_height = int(config[sett.WINDOW_HEIGHT])

        Mover.move_window_to_center(self)

        lm.log_info(sett.CREATE_CREATOR_OBJECT)
        self.creator = Creator(config, self)

        lm.log_info(sett.TRYING_TO_RENDER_WINDOW)
        try:
            self.creator.create_widget_layout(self, config[sett.LAYOUT])
            lm.log_info(sett.SUCCESS)
        except Exception as e:
            lm.log_exception(e)

        if sett.SIZE_BLOCKER in config.keys():
            lm.log_info(sett.BLOCK_SIZE)
            self.setMaximumSize(self.size())
            self.setMinimumSize(self.size())

    def connect_callback(
        self,
        widget: QPushButton | QCheckBox,
        callback_name: str,
        params: dict = {},
        inheritor: Any = None
    ) -> None:
        """
        Привязывает методы наследников (или свои) к различным кнопкам в
        зависимости от их конфига.

        Parameters
        ----------
        - widget: QPushButton | QCheckBox
            Виджет, для которого привязывается метод.

        - callback_name: str,
            Имя метода в виде строки.

        - params: dict
            Default = {}\n
            Параметры для вызова метода (если есть).

        - inheritor: Any
            Default = None\n
            Класс насследник, чьи методы будет использовать виджет.
        """

        match callback_name:
            case sett.CREATE_USER_METHOD:
                widget.clicked.connect(inheritor.create_user)

            case sett.CLOSE_WINDOW_METHOD:
                widget.clicked.connect(lambda: self.cancel(inheritor))

            case sett.TOGGLE_PASSWORD_METHOD:
                widget.stateChanged.connect(
                    lambda: inheritor.toggle_password(widget)
                )

            case sett.TOGGLE_REPEAT_PASSWORD_METHOD:
                widget.stateChanged.connect(
                    lambda: inheritor.toggle_password(
                        widget,
                        sett.REPEAT_PASSWORD
                    )
                )

            case sett.TOGGLE_OLD_PASSWORD_METHOD:
                widget.stateChanged.connect(
                    lambda: inheritor.toggle_password(
                        widget,
                        sett.OLD_PASSWORD
                    )
                )

            case sett.TRY_LOGIN_METHOD:
                widget.clicked.connect(inheritor.try_login)

            case sett.HANDLE_START_BUTTON_METHOD:
                widget.clicked.connect(inheritor.handle_start_button)

            case sett.HANDLE_FORWARD_BUTTON_METHOD:
                widget.clicked.connect(inheritor.handle_forward_button)

            case sett.SAVE_SETTINGS_METHOD:
                widget.clicked.connect(inheritor.save_settings)

            case sett.OPEN_SETTINGS_METHOD:
                widget.clicked.connect(inheritor.open_settings)

            case sett.OPEN_INPUT_WINDOW_METHOD:
                widget.clicked.connect(
                    lambda: inheritor.open_input_window(params)
                )

            case sett.OPEN_REGISTER_METHOD:
                widget.clicked.connect(inheritor.open_register)

            case sett.HANDLE_LOGOUT_METHOD:
                widget.clicked.connect(inheritor.logout)

            case sett.HANDLE_OPEN_MY_PROFILE_METHOD:
                widget.clicked.connect(inheritor.open_my_profile)

            case sett.CHANGE_PASS:
                widget.clicked.connect(inheritor.change_pass)

            case sett.OPEN_DELETE_USER:
                widget.clicked.connect(
                    lambda: inheritor.open_delete_user(params)
                )

            case sett.DELETE_USER:
                widget.clicked.connect(inheritor.delete_user)

            case sett.FORGOT_PASS:
                widget.clicked.connect(
                    lambda: inheritor.forgot_password(params)
                )

            case sett.RECOVER_PASSWORD:
                widget.clicked.connect(inheritor.recover_password)

            case sett.OPEN_USERS_SETTINGS:
                widget.clicked.connect(
                    lambda: inheritor.open_users_settings(params)
                )
            case sett.SAVE_USERS_SETTINGS:
                widget.clicked.connect(inheritor.save_users_settings)

            case sett.CHANGE_EMAIL:
                widget.clicked.connect(inheritor.change_email)

            case sett.CHANGE_PHONE:
                widget.clicked.connect(inheritor.change_phone)

            case sett.CHANGE_NAME:
                widget.clicked.connect(inheritor.change_name)

            case sett.CHANGE_SURNAME:
                widget.clicked.connect(inheritor.change_surname)

            case sett.CHANGE_SEX:
                widget.clicked.connect(inheritor.change_sex)
            case _:
                lm.log_warning(
                    sett.CALLBACK_NOT_FOUND.format(
                        callback_name,
                        widget.objectName()
                    )
                )

    def cancel(self, inheritor: QWidget) -> None:
        """
        В случае, если нажата кнопка `Cancel`, то действия общие для всех этих
        кнопок - записать в лог, что кнопка нажата и закрыть окно
        класса-наследника.

        Parameters
        ----------
        - inheritor: QWidget
            Наследник, окно которого надо закрыть. На самом деле наследники -
            это разные классы и перечислять их здесь нет смысла, но все они
            наследуются от этого класса, а он в свою очередь наследуется от
            QWidget. И поскольку я не могу ссылаться на сам себя, то мне
            пришлось указать QWidget, как тип передаваемого объекта.
        """
        lm.log_info(sett.CANCEL_BUTTON_PRESSED)
        inheritor.close()

    # =========================== Protected methods ===========================
    # -------------------------------------------------------------------------
    def _add_greetings_to_config(self, config: dict) -> None:
        """
        Добавляет в конфиг приветствие для пользователя.

        Parameters
        ----------
        - config: dict
            Конфиг, в который добавляется приветствие.
        """
        lm.log_method_call()

        current_hour = datetime.now().hour

        name = self.userdata.get(
            sett.NAME, sett.EMPTY_STRING
        )

        lm.log_info(sett.SELECT_TIME_OF_DAY)
        if sett.MORNING_HOUR <= current_hour < sett.DAY_HOUR:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_MORNING,
                name
            )
        elif sett.DAY_HOUR <= current_hour < sett.EVENING_HOUR:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_AFTERNOON,
                name
            )
        elif sett.EVENING_HOUR <= current_hour < sett.NIGHT_HOUR:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_EVENING,
                name
            )
        else:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_NIGHT,
                name
            )

        return ConfigGenerator().add_greetings_to_config(
            greeting,
            config
        )
