from gui.auth_window import AuthWindow
from gui.main_window import App
from logic.logger import logger, check_log_size


if __name__ == "__main__":
    import tkinter as tk
    check_log_size()

    logger.info("============================================================")

    root = tk.Tk()
    login_window = AuthWindow(root)
    root.mainloop()

    if login_window.auth_successful:  # ✅ Проверяем успешность авторизации
        root = tk.Tk()
        app = App(root)
        root.mainloop()
    else:
        logger.info("Application closed due to unsuccessful login")
