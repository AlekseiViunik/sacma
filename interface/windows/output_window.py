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
from settings import settings as sett


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
            JsonHandler(sett.OUTPUT_WINDOW_CONFIG_FILE)
        )

    def open_result_window(
        self,
        values: dict,
        pre_message: str | None = None,
        post_message: str | None = None,
        only_keys: list = [sett.PRICE, sett.WEIGHT]
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

        try:
            log.info(sett.CREATE_RESULT_WINDOW)
            log.info(sett.GETTING_CONF_FOR_RESULT_WINDOW)
            log.info(f"The path is {sett.OUTPUT_WINDOW_CONFIG_FILE}")

            # Загружаем конфиг.
            config = self.config_json_handler.get_all_data()
            if config:
                log.info(sett.CONF_DATA_RECEIVED)
                log.info(f"Config is: {config}")
            else:
                log.error(sett.FAILED_GET_JSON_DATA)

            # Настройка окна результатов (Титул, размеры, центрирование).
            self.setWindowTitle(config[sett.WINDOW_TITLE])
            self.window_width = int(config[sett.WINDOW_WIDTH])
            self.window_height = int(config[sett.WINDOW_HEIGHT])
            # Helper.move_window_to_center(self)
            Helper.move_window_to_top_left_corner(self)

            # Настройка главного контейнера по центру окна.
            main_layout = QVBoxLayout()
            main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Создаём шрифт (увеличенный размер)
            font = QFont()
            font.setPointSize(sett.SPECIAL_FONT_SIZE)  # Размер шрифта

            # Размещение сообщения перед результатами, если есть
            if pre_message:
                pre_message_label = QLabel(pre_message)
                pre_message_label.setFont(font)
                pre_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                main_layout.addWidget(pre_message_label)

            # Размещение контейнера-сетки для вывода рензультатов.
            grid_layout = QGridLayout()

            # Фильтруем результат (показываем только нужный) и переводим его.
            filtered_values = {
                k: v for k, v in values.items() if k in only_keys
            }
            filtered_values = Translator.translate_dict(filtered_values)
            row = 0

            # Размещаем лейблы с результатом
            for label, value in filtered_values.items():
                if (
                    (label == sett.PRICE_IT and value) or
                    (label == sett.PREPARATION_IT and value)
                ):
                    value = f"{str(value)} {sett.EURO_SYMBOL}"
                elif label == sett.WEIGHT_IT and value:
                    value = f"{str(value)} {sett.KILO_SYMBOL}"
                elif (
                    label == sett.PRICE_IT or label == sett.WEIGHT_IT
                ) and not value:
                    value = sett.NOT_FOUND_IT

                label = f"{label}: "

                title_label = QLabel(label)
                value_label = QLabel(str(value))

                title_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

                title_label.setFont(font)
                value_label.setFont(font)

                grid_layout.addWidget(title_label, row, sett.SET_TO_ZERO)
                grid_layout.addWidget(value_label, row, sett.SET_TO_ONE)
                row += sett.STEP_UP

            # Добавляем контейнер с лейблами результатов на главный контейнер
            main_layout.addLayout(grid_layout)

            # Размещение сообщения после результатов, если есть
            if (post_message):
                post_message_label = QLabel(post_message)
                post_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                post_message_label.setFont(font)
                main_layout.addWidget(post_message_label)

            # Размещение кнопки ОК
            ok_button = QPushButton(sett.OK_BUTTON_TITLE)
            ok_button.setFixedWidth(sett.OK_BUTTON_WIDTH)
            ok_button.setFixedHeight(sett.OK_BUTTON_HEIGHT)
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
        except Exception as e:
            log.error(f"Error caught: {e}")
