from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from logic.logger import logger as log
from settings import settings as sett


class LabelCreator:
    """
    Класс для создания лейблов.

    Methods
    -------
    - create_label(label_config)
        Создает лейбл по заданному конфигу и возвращает его объект.
    """

    @staticmethod
    def create_label(label_config: dict) -> tuple[QLabel, str | None]:
        """
        Создает, конфигурирует и возвращает объект лейбла.

        Parameters
        ----------
        - label_config: dict
            Конфиг, по которому будет создан и сконфигурирован лейбл.

        Returns
        -------
        - label: QLabel
            Объект созданного лейбла
        """

        log.info(
            sett.CREATE_WIDGET.format(sett.LABEL, label_config[sett.TEXT])
        )
        mandatory_field = None
        label = QLabel()
        font = QFont()
        for param, value in label_config.items():
            match param:
                case sett.TEXT:
                    label.setText(value)
                case sett.TEXT_SIZE:
                    font.setPointSize(label_config[sett.TEXT_SIZE])
                case sett.BOLD:
                    font.setBold(True)
                case sett.ALIGN:
                    # Определяет расположение текста внутри лейбла.
                    if label_config[sett.ALIGN] == sett.ALIGN_CENTER:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if label_config[sett.ALIGN] == sett.ALIGN_LEFT:
                        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    if label_config[sett.ALIGN] == sett.ALIGN_RIGHT:
                        label.setAlignment(Qt.AlignmentFlag.AlignRight)
                case sett.MANDATORY:
                    # Добавляет звездочку в начале текста, если в конфиге
                    # Лейбл помечен как обязательный.
                    text = f"*{label_config[sett.TEXT]}"
                    label.setText(text)
                    mandatory_field = label_config[sett.MANDATORY]
                case sett.WIDTH:
                    label.setFixedWidth(int(value))
                case sett.HEIGHT:
                    label.setFixedHeight(int(value))
                case sett.BACKGROUND:
                    styleSheet = sett.BG_COLOR.format(value)
                    label.setStyleSheet(styleSheet)

        label.setFont(font)
        return label, mandatory_field
