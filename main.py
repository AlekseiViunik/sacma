from gui.auth_window import AuthWindow
from interface.windows.login_window import LoginWindow
from logic.logger import logger, check_log_size
from settings import settings as set


def start_app(window) -> None:
    root = tk.Tk()
    app = window(root)
    root.mainloop()
    return app


if __name__ == "__main__":
    import tkinter as tk
    check_log_size()

    logger.info("============================================================")

    if set.CUSTOM_IMPLEMENTATION:
        from PyQt6.QtWidgets import QApplication
        from interface.custom_app import CustomApp
        import sys

        if set.PRODUCTION_MODE_ON:
            logger.info("Trying to acces the app")
            app = QApplication(sys.argv)
            login_window = LoginWindow()
            login_window.show()
            app.exec()
            if login_window.auth_successful:
                logger.info("Login is successful")
                main_window = CustomApp()
                main_window.show()
                sys.exit(app.exec())
            else:
                logger.info("Application closed due to unsuccessful login")

        else:
            logger.info("Запуск нового интерфейса")
            app = QApplication(sys.argv)
            main_window = CustomApp()
            main_window.show()
            sys.exit(app.exec())
    else:
        from gui.main_window import App
        main_window = App

        if set.PRODUCTION_MODE_ON:
            logger.info("Trying to acces the app")
            login_window = start_app(AuthWindow)

            if login_window.auth_successful:
                # ✅ Проверяем успешность авторизации
                logger.info("Login is successful")
                start_app(main_window)
            else:
                logger.info("Application closed due to unsuccessful login")
        else:
            start_app(main_window)
