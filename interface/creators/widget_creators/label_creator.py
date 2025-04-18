from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

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

                # Выравнивание текста по горизонтали.
                case sett.ALIGN:
                    if label_config[sett.ALIGN] == sett.ALIGN_CENTER:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if label_config[sett.ALIGN] == sett.ALIGN_LEFT:
                        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    if label_config[sett.ALIGN] == sett.ALIGN_RIGHT:
                        label.setAlignment(Qt.AlignmentFlag.AlignRight)

                # Выравнивание текста по вертикали.
                case sett.ALIGNV:
                    if label_config[sett.ALIGNV] == sett.ALIGN_CENTER:
                        label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

                # Добавляет звездочку в начале текста, если в конфиге
                # Лейбл помечен как обязательный.
                case sett.MANDATORY:
                    text = sett.MANDATORY_FIELD_LABEL.format(
                        label_config[sett.TEXT]
                    )
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
