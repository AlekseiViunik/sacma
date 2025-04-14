import ctypes

from datetime import datetime

from interface.windows.login_window import LoginWindow
from logic.handlers.excel_handler import ExcelHandler
from logic.helpers.backuper import Backuper
from logic.generators.filepath_generator import FilepathGenerator
from logic.logger import logger, check_log_size, switch_log_to_user
from logic.protectors.protector import Protector
from logic.protectors.config_protector import ConfigProtector
from settings import settings as sett


if __name__ == "__main__":

    def launch_app(username: str | None = None) -> None:
        """
        Запускает приложение с указанным именем пользователя.
        Если имя пользователя не указано, запускает приложение без него.

        Parameters
        ----------
        - username: str | None
            Default = None\n
            Имя пользователя, с которым будет запущено приложение.
            Если None, приложение запускается с именем создателя по
            умолчанию.
        """
        user_settings_path = FilepathGenerator.generate_settings_filepath(
            sett.SETTINGS_FILE, username
        )

        excel_handler = ExcelHandler(settings_file_path=user_settings_path)
        if not excel_handler.check_excel_file():
            sys.exit()

        if not sett.TEST_GUI:
            excel_handler.open_excel()
            app.aboutToQuit.connect(excel_handler.close_excel)
            app.aboutToQuit.connect(
                lambda: ConfigProtector.protect_all_json_files(
                    sett.CONFIGS_FOLDER
                )
            )
        main_window = StartWindow(
            username=username,
            excel_handler=excel_handler,
            user_settings_path=user_settings_path
        )
        main_window.show()
        sys.exit(app.exec())

    check_log_size()

    if sett.PRODUCTION_MODE_ON:
        protector = Protector(
            deadline=datetime(
                sett.PROTECTION_4,
                sett.PROTECTION_2,
                sett.PROTECTION_1,
                sett.PROTECTION_3,
                sett.SET_TO_ZERO,
                sett.SET_TO_ZERO
            )
        )
        protector.activate()

    Backuper.backup_files(
        sett.SETTINGS_FILE,
        sett.CONFIGS_FOLDER,
        sett.BACKUPS_FOLDER
    )

    logger.info("============================================================")

    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from interface.start_window import StartWindow
    import sys

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        sett.SACMA_APP
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(sett.ICON_PATH))

    if sett.PRODUCTION_MODE_ON:
        ConfigProtector.protect_all_json_files(sett.CONFIGS_FOLDER)
        logger.info(sett.TRYING_LOGIN)
        login_window = LoginWindow()
        if login_window.exec():
            logger.info(sett.SUCCESSFUL_LOGIN)
            # Меняем файл логов на файл с именем пользователя
            switch_log_to_user(login_window.username)

            # Запускаем приложение с именем пользователя
            launch_app(username=login_window.username)
        else:
            logger.info(sett.UNSUCCESSFUL_LOGIN)
            sys.exit()

    else:
        ConfigProtector.unprotect_all_json_files(sett.CONFIGS_FOLDER)
        logger.info(sett.NEW_APP_START)
        launch_app(username=sett.ALEX)
