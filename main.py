from interface.windows.login_window import LoginWindow
from logic.logger import logger, check_log_size
from settings import settings as set


if __name__ == "__main__":
    check_log_size()

    logger.info("============================================================")

    from PyQt6.QtWidgets import QApplication
    from interface.start_window import StartWindow
    import sys

    if set.PRODUCTION_MODE_ON:
        logger.info("Trying to acces the app")
        app = QApplication(sys.argv)
        login_window = LoginWindow()
        login_window.show()
        app.exec()
        if login_window.auth_successful:
            logger.info("Login is successful")
            main_window = StartWindow()
            main_window.show()
            sys.exit(app.exec())
        else:
            logger.info("Application closed due to unsuccessful login")

    else:
        logger.info("Запуск нового интерфейса")
        app = QApplication(sys.argv)
        main_window = StartWindow()
        main_window.show()
        sys.exit(app.exec())
