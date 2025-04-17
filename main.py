import ctypes

from datetime import datetime

from interface.windows.info_window import InfoWindow
from interface.windows.login_window import LoginWindow
from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.dropbox_handler import DropboxHandler
from logic.helpers.backuper import Backuper
from logic.generators.filepath_generator import FilepathGenerator
from logic.logger import LogManager as lm
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
        lm.log_method_call()

        user_settings_path = FilepathGenerator.generate_settings_filepath(
            sett.SETTINGS_FILE, username
        )

        excel_handler = ExcelHandler()
        dropbox = DropboxHandler(excel_handler, user_settings_path)

        if not sett.TEST_GUI:
            dialog = InfoWindow()
            dialog.show()
            QApplication.processEvents()

            dropbox.open_excel()
            dialog.accept()

            app.aboutToQuit.connect(dropbox.close_excel)
            app.aboutToQuit.connect(
                lambda: ConfigProtector.protect_all_json_files(
                    sett.CONFIGS_FOLDER
                )
            )

        main_window = StartWindow(
            username=username,
            excel_handler=excel_handler,
            dropbox_handler=dropbox,
            user_settings_path=user_settings_path
        )

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

    lm.log_info("============================================================")
    Backuper.backup_files(
       sett.SETTINGS_FILE,
       sett.CONFIGS_FOLDER,
       sett.BACKUPS_FOLDER
    )

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
        lm.log_info(sett.TRYING_LOGIN)
        login_window = LoginWindow()
        if login_window.exec():
            lm.log_info(sett.SUCCESSFUL_LOGIN)
            # Меняем файл логов на файл с именем пользователя
            lm.switch_log_to_user(login_window.username)

            # Запускаем приложение с именем пользователя
            launch_app(username=login_window.username)
        else:
            lm.log_info(sett.UNSUCCESSFUL_LOGIN)
            sys.exit()

    else:
        ConfigProtector.unprotect_all_json_files(sett.CONFIGS_FOLDER)
        launch_app(username=sett.ALEX)
