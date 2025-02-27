from gui.main_window import App
from logic.logger import logger, check_log_size

if __name__ == "__main__":
    import tkinter as tk
    check_log_size()
    logger.info("============================================================")

    root = tk.Tk()
    app = App(root)
    root.mainloop()
