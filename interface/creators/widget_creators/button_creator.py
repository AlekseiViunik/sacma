from PyQt6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

from settings import settings as sett

if TYPE_CHECKING:
    from interface.windows.base_window import BaseWindow


class ButtonCreator:
    """
    Класс для создания кнопок.

    Methods
    -------
    - create_button(button_config, parent_window)
        Создает кнопку по заданному конфигу и возвращает ее объект.
    """

    @staticmethod
    def create_button(
        button_config: dict,
        # Кавычки нужны, чтобы избежать циклической зависимости
        parent_window: "BaseWindow"
    ) -> QPushButton:
        """
        Создает, конфигурирует и возвращает объект кнопки.

        Parameters
        ----------
        - config: dict
            Конфиг, по которому будет создана и сконфигурирована кнопка.
        - parent_window: BaseWindow
            Родительское окно, к которому будет привязана кнопка.

        Returns
        -------
        - button: QPushButton
            Объект созданной кнопки.
        """

        button = QPushButton(button_config[sett.TEXT])
        for param, value in button_config.items():
            match param:
                case sett.WIDTH:
                    button.setFixedWidth(int(value))
                case sett.HEIGHT:
                    button.setFixedHeight(int(value))
                case sett.CALLBACK:
                    parent_window.connect_callback(
                        button,
                        value,
                        button_config.get(sett.PARAMS, {}),
                        parent_window
                    )
                case sett.ALLOWED_TO_GROUPS:
                    user_group = parent_window.userdata.get(sett.GROUP)
                    if user_group not in value:
                        button.setEnabled(False)

                case sett.BUTTON_COLOR:
                    button.setStyleSheet(
                        sett.BG_COLOR.format(value)
                    )

        # Активирует кнопку, только если в ее конфиге есть коллбэк.
        button.setObjectName(button_config[sett.TEXT])
        if sett.CALLBACK not in button_config:
            button.setEnabled(False)
        return button
