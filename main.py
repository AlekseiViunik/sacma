from datetime import datetime

from interface.windows.login_window import LoginWindow
from logic.logger import logger, check_log_size
from logic.protector import Protector
from settings import settings as sett


if __name__ == "__main__":
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

    if sett.PRODUCTION_MODE_ON:
        logger.info(sett.TRYING_LOGIN)
        app = QApplication(sys.argv)
        login_window = LoginWindow()
        if login_window.exec():
            logger.info(sett.SUCCESSFUL_LOGIN)

            main_window = StartWindow(login_window.username)
            main_window.show()
            sys.exit(app.exec())
        else:
            logger.info(sett.UNSUCCESSFUL_LOGIN)

    else:
        logger.info(sett.NEW_APP_START)
        app = QApplication(sys.argv)
        main_window = StartWindow()
        main_window.show()
        sys.exit(app.exec())
