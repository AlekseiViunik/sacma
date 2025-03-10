from gui.auth_window import AuthWindow
from gui.main_window import App
from logic.logger import logger, check_log_size
from settings import settings as set


def start_app(window: AuthWindow | App) -> None:
    root = tk.Tk()
    app = window(root)
    root.mainloop()
    return app


if __name__ == "__main__":
    import tkinter as tk
    check_log_size()

    logger.info("============================================================")

    if set.PRODUCTION_MODE_ON:
        logger.info("Trying to acces the app")
        login_window = start_app(AuthWindow)

        if login_window.auth_successful:
            # ✅ Проверяем успешность авторизации
            logger.info("Login is successful")
            start_app(App)
        else:
            logger.info("Application closed due to unsuccessful login")
    else:
        start_app(App)
