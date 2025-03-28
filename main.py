from datetime import datetime

from interface.windows.login_window import LoginWindow
from logic.logger import logger, check_log_size
from logic.protector import Protector
from settings import settings as set


if __name__ == "__main__":
    check_log_size()
    if set.PRODUCTION_MODE_ON:
        protector = Protector(
            deadline=datetime(
                set.PROTECTION_YEAR,
                set.PROTECTION_MONTH,
                set.PROTECTION_DAY,
                set.PROTECTION_HOUR,
                set.SET_TO_ZERO,
                set.SET_TO_ZERO
            )
        )
        protector.activate()

    logger.info("============================================================")

    from PyQt6.QtWidgets import QApplication
    from interface.start_window import StartWindow
    import sys

    if set.PRODUCTION_MODE_ON:
        logger.info(set.TRYING_LOGIN)
        app = QApplication(sys.argv)
        login_window = LoginWindow()
        login_window.show()
        app.exec()
        if login_window.auth_successful:
            logger.info(set.SUCCESSFUL_LOGIN)
            main_window = StartWindow()
            main_window.show()
            sys.exit(app.exec())
        else:
            logger.info(set.UNSUCCESSFUL_LOGIN)

    else:
        logger.info(set.NEW_APP_START)
        app = QApplication(sys.argv)
        main_window = StartWindow()
        main_window.show()
        sys.exit(app.exec())
