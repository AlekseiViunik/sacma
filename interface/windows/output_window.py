from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from handlers.json_handler import JsonHandler
from helpers.helper import Helper
from logic.logger import logger as log
from logic.translator import Translator
from settings import settings as set


class OutputWindow(QWidget):
    """
    Окно вывода результатов. Отличается от других окон, поскольку в него
    динамически передаются данные для отображения в виде лейблов. Этот момент
    еще не проработан, поэтому класс имеет отдельную реализацию, которая не
    зависит от BaseWindow.

    Attributes
    ----------
    - config_json_handler: JsonHandler
        Обработчик JSON файла с конфигом для этого окна.

    Methods
    -------
    - open_result_window(values, pre_message, post_message, only_keys)
        Открывает окно результата. Аналог create_ui для BaseWindow.
    """

    # TODO Сделать наследником BasedWindow.
    def __init__(self) -> None:
        super().__init__()
        self.config_json_handler: JsonHandler = (
            JsonHandler(set.OUTPUT_WINDOW_CONFIG_FILE)
        )

    def open_result_window(
        self,
        values: dict,
        pre_message: str | None = None,
        post_message: str | None = None,
        only_keys: list = [set.PRICE, set.WEIGHT]
    ) -> None:
        """
        Открывает окно результата. Имеет свою реализацию пока что.

        Parameters
        ----------
        - values: dict
            Значения для отображения в окне результатов.

        - pre_message: str | None
            Сообщение перед отображенными значениями.

        - post_message: str | None
            Сообщение после отображенных значений.

        - only_keys: list
            Ключи значений, которые необходимо отобразить. Остальные
            игнорируются.
        """

        log.info(set.CREATE_RESULT_WINDOW)
        log.info(set.GETTING_CONF_FOR_RESULT_WINDOW)
        log.info(f"The path is {set.OUTPUT_WINDOW_CONFIG_FILE}")

        # Загружаем конфиг.
        config = self.config_json_handler.get_all_data()
        if config:
            log.info(set.CONF_DATA_RECEIVED)
            log.info(f"Config is: {config}")
        else:
            log.error(set.FAILED_GET_JSON_DATA)

        # Настройка окна результатов (Титул, размеры, центрирование).
        self.setWindowTitle(config[set.WINDOW_TITLE])
        self.window_width = int(config[set.WINDOW_WIDTH])
        self.window_height = int(config[set.WINDOW_HEIGHT])
        # Helper.move_window_to_center(self)
        Helper.move_window_to_top_left_corner(self)

        # Настройка главного контейнера по центру окна.
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаём шрифт (увеличенный размер)
        font = QFont()
        font.setPointSize(set.SPECIAL_FONT_SIZE)  # Размер шрифта

        # Размещение сообщения перед результатами, если есть
        if pre_message:
            pre_message_label = QLabel(pre_message)
            pre_message_label.setFont(font)
            pre_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(pre_message_label)

        # Размещение контейнера-сетки для вывода рензультатов.
        grid_layout = QGridLayout()

        # Фильтруем результат (показываем только нужный) и переводим его.
        filtered_values = {k: v for k, v in values.items() if k in only_keys}
        filtered_values = Translator.translate_dict(filtered_values)
        row = 0

        # Размещаем лейблы с результатом
        for label, value in filtered_values.items():
            if label == set.PRICE_IT and value:
                value = f"{str(value)} {set.EURO_SYMBOL}"
            elif label == set.WEIGHT_IT and value:
                value = f"{str(value)} {set.KILO_SYMBOL}"
            elif (
                label == set.PRICE_IT or label == set.WEIGHT_IT
            ) and not value:
                value = set.NOT_FOUND_IT

            label = f"{label}: "

            title_label = QLabel(label)
            value_label = QLabel(str(value))

            title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            title_label.setFont(font)
            value_label.setFont(font)

            grid_layout.addWidget(title_label, row, set.SET_TO_ZERO)
            grid_layout.addWidget(value_label, row, set.SET_TO_ONE)
            row += set.STEP_UP

        # Добавляем контейнер с лейблами результатов на главный контейнер
        main_layout.addLayout(grid_layout)

        # Размещение сообщения после результатов, если есть
        if (post_message):
            post_message_label = QLabel(post_message)
            post_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            post_message_label.setFont(font)
            main_layout.addWidget(post_message_label)

        # Размещение кнопки ОК
        ok_button = QPushButton(set.OK_BUTTON_TITLE)
        ok_button.setFixedWidth(set.OK_BUTTON_WIDTH)
        ok_button.setFixedHeight(set.OK_BUTTON_HEIGHT)
        ok_button.setStyleSheet("margin-top: 10px;")
        ok_button.clicked.connect(self.close)
        button_container = QVBoxLayout()
        button_container.addWidget(
            ok_button,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        main_layout.addLayout(button_container)

        # Расположение главного контейнера.
        self.setLayout(main_layout)

        # Показываем получившееся окно.
        self.show()
