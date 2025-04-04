from datetime import datetime

from typing import Any
from PyQt6.QtWidgets import QWidget, QPushButton, QCheckBox
from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from logic.config_generator import ConfigGenerator
from logic.logger import logger as log
from settings import settings as sett


class BaseWindow(QWidget):
    """
    Базовое окно для всех окон приложения.

    Attributes
    ----------
    - window_width: int
        Начальная ширина окна класса-наследника.

    - window_height: int
        Начальная высота окна класса-наследника.

    - config_json_handler: JsonHandler
        Обработчик JSON файла с конфигом, содержащим информацию о виджетах.

    - creator: Creator | None
        Класс, используемый для создания и размещения виджетов и контейнеров.

    Methods
    -------
    - init_ui()
        Метод отрисовки интерфейса окна. Использует Креатор.

    - connect_callback(widget, callback_name, params, inheritor)
        Привязывает методы наследников (или свои) к кнопкам по их конфигу.

    - cancel(inheritor)
        Свой метод для кнопки Cancel. Закрывает окно и пишет об этом в лог.
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
        - Настраивает Титул и размеры окна.
        - Перемещает окно в центр экрана.
        - Размещает виджеты, используя креатор.
        """

        log.info(sett.CREATE_WINDOW_WITH_CONF.format(self.CONFIG_FILE))

        # Загружаем конфиг
        config = self.config_json_handler.get_all_data()

        if config:
            log.info(sett.CONFIG_LOADED_SUCCESSFULLY.format(config))
        else:
            log.error(sett.FAILED_GET_JSON_DATA)

        if config.get(sett.WINDOW_TITLE) == sett.SACMA:
            config = self._add_greetings_to_config(config)

        self.setWindowTitle(config[sett.WINDOW_TITLE])
        self.window_width = int(config[sett.WINDOW_WIDTH])
        self.window_height = int(config[sett.WINDOW_HEIGHT])

        Helper.move_window_to_top_left_corner(self)

        log.info(sett.USE_CREATOR)
        self.creator = Creator(config, self)
        try:
            self.creator.create_widget_layout(self, config[sett.LAYOUT])
        except Exception as e:
            Helper.log_exception(e)

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

        - params: dict = {},
            Параметры для вызова метода (если есть).

        - inheritor: Any = None
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

            case sett.BROWSE_FILE_METHOD:
                target_input = params.get(sett.TARGET_INPUT)
                widget.clicked.connect(
                    lambda: inheritor.browse_file(target_input)
                )

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

            case sett.HANDLE_CHANGE_PASS_METHOD:
                widget.clicked.connect(inheritor.change_password)

            case sett.CHANGE_PASS:
                widget.clicked.connect(inheritor.change_pass)

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

        log.info(sett.CANCEL_BUTTON_PRESSED)
        inheritor.close()

    def _add_greetings_to_config(self, config: dict) -> None:
        """
        Добавляет в конфиг приветствие для пользователя.

        Parameters
        ----------
        - config: dict
            Конфиг, в который добавляется приветствие.
        """
        current_hour = datetime.now().hour

        if sett.MORNING_HOUR <= current_hour < sett.DAY_HOUR:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_MORNING,
                self.userdata[sett.SURNAME]
            )
        elif sett.DAY_HOUR <= current_hour < sett.EVENING_HOUR:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_MORNING,
                self.userdata[sett.SURNAME]
            )
        elif sett.EVENING_HOUR <= current_hour < sett.NIGHT_HOUR:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_MORNING,
                self.userdata[sett.SURNAME]
            )
        else:
            greeting = sett.GREETING_MSG.format(
                sett.GOOD_MORNING,
                self.userdata[sett.SURNAME]
            )

        return ConfigGenerator().add_greetings_to_config(
            greeting,
            config
        )
