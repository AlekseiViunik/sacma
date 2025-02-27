from gui.main_window import App
from logic.logger import logger

if __name__ == "__main__":
    import tkinter as tk
    logger.info("============================================================")

    root = tk.Tk()
    app = App(root)
    root.mainloop()
