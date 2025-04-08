from PyQt6.QtWidgets import QCheckBox
from typing import TYPE_CHECKING

from logic.logger import logger as log
from settings import settings as sett

if TYPE_CHECKING:
    from interface.windows.base_window import BaseWindow


class CheckboxCreator:

    @staticmethod
    def create_checkbox(
        checkbox_config: dict,
        # Кавычки нужны, чтобы избежать циклической зависимости
        parent_window: "BaseWindow"
    ) -> QCheckBox:
        """
        Создает, конфигурирует и возвращает объект чекбокса.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создан и сконфигурирован чекбокс.

        Returns
        -------
        - checkbox: QCheckBox
            Объект созданного чекбокса.
        """

        log.info(
            sett.CREATE_WIDGET.format(
                sett.CHECKBOX, checkbox_config[sett.NAME]
            )
        )
        checkbox = QCheckBox()
        for param, value in checkbox_config.items():
            match param:
                case sett.TEXT:
                    checkbox.setText(value)
                case sett.CALLBACK:
                    # Привязка метода, который будет вызван при
                    # активации/деактивации чекбокса.
                    parent_window.connect_callback(
                        checkbox,
                        value,
                        checkbox_config.get(sett.PARAMS, {}),
                        parent_window
                    )
        return checkbox
