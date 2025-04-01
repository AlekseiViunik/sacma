from PyQt6.QtWidgets import (
    QLineEdit,
    QFileDialog
)

from .base_window import BaseWindow
from handlers.json_handler import JsonHandler
from helpers.helper import Helper
from logic.logger import logger as log
from settings import settings as sett


class SettingsWindow(BaseWindow):
    """
    Окно настроек.

    Attributes
    ----------
    - settings_json_handler: JsonHandler
        Обработчик JSON файла, хранящего пользовательские настройки.

    Methods
    -------
    - browse_file(target_input)
        Открывает окно выбора файла

    - save_settings()
        Переписывает файл настроек и закрывает окно.
    """

    CONFIG_FILE = sett.SETTINGS_WINDOW_CONFIG_FILE

    def __init__(self) -> None:
        super().__init__()
        self.settings_json_handler = JsonHandler(sett.SETTINGS_FILE)

        self.init_ui()

    def browse_file(self, target_input: QLineEdit) -> None:
        """
        Метод, срабатывающий при нажатии кнопки Browse. Открывает окно выбора
        файла excel.

        Parameters
        ----------
        - target_input: QLineEdit
            Поле для ввода, в которое будет вставлен выбранный путь к файлу.
        """

        log.info(sett.BROWSE_BUTTON_PRESSED)

        # Получаем путь к файлу, выбрав его в открывшемся окне.
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            sett.CHOSE_FILE,
            sett.EMPTY_STRING,
            sett.EXCEL_FILES_FILTER
        )

        # Если путь получен и поле для ввода находится массива полей для ввода
        # у креатора, то меняем у этого поля для ввода отображаемый введенный
        # текст на путь к файлу.
        if file_path and target_input in self.creator.input_fields:
            self.creator.input_fields[target_input].setText(file_path)
            self.creator.input_fields[target_input].setPlaceholderText(
                file_path
            )

    def save_settings(self) -> None:
        """
        Переписывает файл настроек и закрывает окно.
        """

        try:
            log.info(sett.SAVE_BUTTON_PRESSED)
            log.info(sett.TRYING_TO_REWRITE_SETTINGS)
            log.info(sett.PATH_IS.format(sett.SETTINGS_FILE))
            log.info(sett.REWRITING_CHECK_IS_UNAVAILABLE)
            self.settings_json_handler.rewrite_file(
                self.creator.input_fields
            )
            self.close()

        except Exception as e:
            Helper.log_exception(e)
