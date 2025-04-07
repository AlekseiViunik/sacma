from datetime import datetime

from handlers.excel_handler import ExcelHandler
from handlers.json_handler import JsonHandler
from interface.windows.login_window import LoginWindow
from interface.windows.settings_window import SettingsWindow
from logic.logger import logger, check_log_size
from logic.protector import Protector
from settings import settings as sett


if __name__ == "__main__":

    def check_excel_file() -> None:
        """
        Проверяет, существует ли файл Excel, указанный в настройках.
        Если файла нет, открывает окно настроек.
        """
        settings_json_handler = JsonHandler(sett.SETTINGS_FILE)
        while not settings_json_handler.get_value_by_key(sett.EXCEL_PATH):
            logger.info(sett.SETTINGS_BUTTON_PRESSED)
            settings_window = SettingsWindow()
            result = settings_window.exec()
            if result == 0:  # пользователь нажал Cancel (reject)
                return False
        return True

    def launch_app(username: str | None = None) -> None:
        """
        Запускает приложение с указанным именем пользователя.
        Если имя пользователя не указано, запускает приложение без него.
        """
        if not check_excel_file():
            logger.info("User cancelled settings — exiting app.")
            sys.exit()
        excel_handler = ExcelHandler()
        excel_handler.open_excel()
        app.aboutToQuit.connect(excel_handler.close_excel)
        main_window = StartWindow(
            username=username,
            excel_handler=excel_handler
        )
        main_window.show()
        sys.exit(app.exec())

    check_log_size()
    if sett.PRODUCTION_MODE_ON:
        protector = Protector(
            deadline=datetime(
                sett.PROTECTION_YEAR,
                sett.PROTECTION_MONTH,
                sett.PROTECTION_DAY,
                sett.PROTECTION_HOUR,
                sett.SET_TO_ZERO,
                sett.SET_TO_ZERO
            )
        )
        protector.activate()

    logger.info("============================================================")

    from PyQt6.QtWidgets import QApplication
    from interface.start_window import StartWindow
    import sys

    app = QApplication(sys.argv)

    if sett.PRODUCTION_MODE_ON:
        logger.info(sett.TRYING_LOGIN)
        login_window = LoginWindow()
        if login_window.exec():
            logger.info(sett.SUCCESSFUL_LOGIN)
            launch_app(username=login_window.username)
        else:
            logger.info(sett.UNSUCCESSFUL_LOGIN)
            sys.exit()

    else:
        logger.info(sett.NEW_APP_START)
        launch_app(username=sett.ALEX)
