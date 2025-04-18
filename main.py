import ctypes
import sys

from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from interface.start_window import StartWindow
from interface.windows.info_window import InfoWindow
from interface.windows.login_window import LoginWindow
from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.dropbox_handler import DropboxHandler
from logic.helpers.backuper import Backuper
from logic.generators.filepath_generator import FilepathGenerator
from logic.logger import LogManager as lm
from logic.protectors.config_protector import ConfigProtector
from logic.protectors.protector import Protector
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
        lm.log_method_call()

        user_settings_path = FilepathGenerator.generate_settings_filepath(
            sett.SETTINGS_FILE, username
        )
        lm.log_info(sett.USER_SETTINGS_PATH_IS, user_settings_path)

        lm.log_info(sett.CREATE_EXCEL_HANDLER_OBJECT)
        excel_handler = ExcelHandler()

        lm.log_info(sett.CREATE_DROPBOX_HANDLER_OBJECT)
        dropbox = DropboxHandler(excel_handler, user_settings_path)

        if not sett.TEST_GUI:

            lm.log_info(sett.SHOW_LOADING_WINDOW)
            dialog = InfoWindow()
            dialog.show()
            QApplication.processEvents()

            lm.log_info(sett.TRYING_TO_OPEN_EXCEL)
            dropbox.open_excel()

            lm.log_info(sett.CLOSE_LOADING_WINDOW)
            dialog.accept()

            lm.log_info(sett.SET_ABOUT_TO_QUIT_CASE)
            app.aboutToQuit.connect(dropbox.close_excel)
            app.aboutToQuit.connect(
                lambda: ConfigProtector.protect_all_json_files(
                    sett.CONFIGS_FOLDER
                )
            )
        else:
            lm.log_info(sett.TEST_GUI_MODE)

        lm.log_info(sett.CREATE_MAIN_WINDOW)
        main_window = StartWindow(
            username=username,
            excel_handler=excel_handler,
            dropbox_handler=dropbox,
            user_settings_path=user_settings_path
        )

        lm.log_info(sett.SHOW_MAIN_WINDOW)
        main_window.show()
        sys.exit(app.exec())

    lm.setup_default_logger()
    lm.check_log_size()

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

    lm.log_info(sett.LOG_DELIMITER)
    lm.log_info(sett.TRYING_BACKUP)
    try:
        Backuper.backup_files(
            sett.SETTINGS_FILE,
            sett.CONFIGS_FOLDER,
            sett.BACKUPS_FOLDER
        )
    except Exception as e:
        lm.log_exception(e)

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        sett.SACMA_APP
    )

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(sett.ICON_PATH))

    if sett.PRODUCTION_MODE_ON:
        lm.log_info(sett.TEST_MODE_OFF)
        lm.log_info(sett.PROTECTING_FILES, sett.CONFIGS_FOLDER)
        ConfigProtector.protect_all_json_files(sett.CONFIGS_FOLDER)
        lm.log_info(sett.TRYING_LOGIN)

        lm.log_info(sett.CREATE_LOGIN_WINDOW)
        login_window = LoginWindow()
        if login_window.exec():
            lm.log_info(sett.SUCCESSFUL_LOGIN)
            # Меняем файл логов на файл с именем пользователя
            lm.switch_log_to_user(login_window.username)

            lm.log_info(sett.LOG_DELIMITER)
            lm.log_info(sett.LAUNCH_APP, login_window.username)
            # Запускаем приложение с именем пользователя
            launch_app(username=login_window.username)
        else:
            lm.log_info(sett.UNSUCCESSFUL_LOGIN)
            sys.exit()

    else:
        lm.log_info(sett.TEST_MODE_ON)
        lm.switch_log_to_user(sett.ALEX)
        lm.log_info(sett.LOG_DELIMITER)
        lm.log_info(sett.TRYING_TO_UNPROTECT_FILES, sett.CONFIGS_FOLDER)
        try:
            ConfigProtector.unprotect_all_json_files(sett.CONFIGS_FOLDER)
        except Exception as e:
            lm.log_exception(e)
        lm.log_info(sett.LAUNCH_APP, sett.ALEX)
        launch_app(username=sett.ALEX)
