from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from settings import settings as sett


class ImageCreator:
    """
    Класс для создания картинок в лейбле.

    Methods
    -------
    - create_image(image_config)
        Создает лейбл с картинкой по заданному конфигу и возвращает его объект.
    """

    @staticmethod
    def create_image(image_config: dict) -> QLabel:
        """
        Создает, конфигурирует и возвращает объект лейбла с картинкой.

        Parameters
        ----------
        - image_config: dict
            Конфиг, по которому будет создан и сконфигурирован лейбл.

        Returns
        -------
        - label: QLabel
            Объект созданного лейбла с картинкой
        """

        label = QLabel()
        pixmap = QPixmap(sett.EMPTY_STRING)
        for param, value in image_config.items():
            match param:
                case sett.ALIGN:
                    # Определяет расположение текста внутри лейбла.
                    if image_config[sett.ALIGN] == sett.ALIGN_CENTER:
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if image_config[sett.ALIGN] == sett.ALIGN_LEFT:
                        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    if image_config[sett.ALIGN] == sett.ALIGN_RIGHT:
                        label.setAlignment(Qt.AlignmentFlag.AlignRight)
                case sett.SCALED_CONTENTS:
                    label.setScaledContents(True)
                case sett.PATH:
                    pixmap = QPixmap(value)
        label.setPixmap(pixmap)

        return label
