from typing import Any
from PyQt6.QtWidgets import QWidget, QPushButton, QCheckBox
from handlers.json_handler import JsonHandler
from interface.creator import Creator
from helpers.helper import Helper
from logic.logger import logger as log


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

    - connect_callback()
        Привязывает методы наследников (или свои) к кнопкам по их конфигу.

    - cancel()
        Свой метод для кнопки Cancel. Закрывает окно и пишет об этом в лог.
    """

    CONFIG_FILE = None  # Путь к конфигу должен задаваться в наследниках

    def __init__(
        self,
        file_path: str | None = None
    ) -> None:
        super().__init__()
        self.window_width: int = 0
        self.window_height: int = 0

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

        log.info(f"Creating window with config: {self.CONFIG_FILE}")

        # Загружаем конфиг
        config = self.config_json_handler.get_all_data()

        if config:
            log.info(f"Config loaded successfully: {config}")
        else:
            log.error("Couldn't get the data from the file!")
            return

        self.setWindowTitle(config['window_title'])
        self.window_width = int(config['window_width'])
        self.window_height = int(config['window_height'])

        Helper.move_window_to_top_left_corner(self)

        log.info("Using creator to generate UI layout")
        self.creator = Creator(config, self)
        self.creator.create_widget_layout(self, config["layout"])

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
            case "create_user":
                widget.clicked.connect(inheritor.create_user)

            case "close_window":
                widget.clicked.connect(lambda: self.cancel(inheritor))

            case "toggle_password":
                widget.stateChanged.connect(
                    lambda: inheritor.toggle_password(widget)
                )
            case "toggle_repeat_password":
                widget.stateChanged.connect(
                    lambda: inheritor.toggle_password(
                        widget,
                        "repeat_password"
                    )
                )
            case "try_login":
                widget.clicked.connect(inheritor.try_login)

            case "handle_start_button":
                widget.clicked.connect(inheritor.handle_start_button)

            case "browse_file":
                target_input = params.get("target_input")
                widget.clicked.connect(
                    lambda: inheritor.browse_file(target_input)
                )
            case "save_settings":
                widget.clicked.connect(inheritor.save_settings)

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

        log.info("Cancel button has been pressed")
        inheritor.close()
