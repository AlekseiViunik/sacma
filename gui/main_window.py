import math
import tkinter as tk
import os
import sys
import ctypes

from PIL import Image, ImageTk

from .helper import Helper
from logic.logger import logger as log
from settings import settings as set


class App:
    """Класс App используется для создания основного окна.

    Основное применение - создание главного окна приложения и его кнопок,
    Запус процесса обработки входных данных и вывод результата в отдельном
    окне. Во время инициализации сразу же вызывает метод раскидывания виджетов
    по окну.

    Attributes
    ----------
    root : tk.Tk
        Главное окно.
    entries : Dict
        список введенных значений.
    buttons : List[String]
        список кнопок, размещаемых на главном окне.

    Methods
    -------
    create_widgets()
        Раскидывает виджеты по главному окну.
    open_window(name)
        Открывает второстепенное окно с базовыми виджетами, одинаковыми для
        всех такого рода окон.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.resizable(False, False)
        self.entries = {}
        self.root.title(f"{set.MAIN_WIN_TITLE}")
        self.root.geometry(f"{set.MAIN_WIN_WIDTH}x{set.MAIN_WIN_HEIGHT}")
        self.buttons = set.MAIN_WIN_BUTTONS
        Helper.center_window(
            set.MAIN_WIN_WIDTH,
            set.MAIN_WIN_HEIGHT,
            self.root
        )

        self.set_window_icon()
        self.create_widgets()

    def create_widgets(self) -> None:
        """Создает виджеты для главного окна. Сами виджеты подразумевают под
        собой фреймы, кнопки, лейблы. Вызывать не надо - вызывается
        автоматически."""

        log.info("Create widgets on main window")
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        cols = set.COL_NUM
        rows = math.ceil(len(self.buttons) / cols)

        max_width = max(len(name) for name in self.buttons)

        for i, name in enumerate(self.buttons):
            btn = tk.Button(
                frame,
                text=name,
                height=set.BUTTON_HEIGHT,
                width=max_width,
                bg=set.BUTTON_COLOR,
                relief=set.BUTTON_RELIEF,
                command=lambda n=name: self.open_window(n)
            )
            btn.grid(
                row=i // cols,
                column=i % cols,
                padx=set.BUTTON_PADX,
                pady=set.BUTTON_PADY,
                sticky=set.BUTTON_STICKY
            )

        for i in range(cols):
            self.root.columnconfigure(i, weight=set.GRID_WEIGHT)
        for i in range(rows):
            self.root.rowconfigure(i, weight=set.GRID_WEIGHT)

    def open_window(self, name: str) -> None:
        """Открывает базу второстепенного окна фреймом и кнопкой Invia.
        В зависимости от того, какая кнопка была нажата, вызывает частный
        вспомогательный метод для отрисовки компонентов. Будет работать,
        только если существует модуль с классом, имя которого совпадает с
        переданным в параметры именем.

        Parameters
        ----------
            name: str
                Имя окна. От него же зависит начинка окна виджетами.
        """

        class_name = Helper.get_class_name_if_exists(name)
        instance = class_name(self.root, name) if class_name else None
        if instance:
            instance.open_window()
        else:
            log.info(f"Class {instance} not found!")

    def set_window_icon(self):
        """Sets up the window icons."""
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            'SACMA'
        )

        if getattr(sys, 'frozen', False):
            # If it run as an executable file
            icon_path_png = os.path.join(
                sys._MEIPASS,
                set.ICONS_FOLDER_NAME,
                set.PNG_ICON_FILENAME
            )
            icon_path_ico = os.path.join(
                sys._MEIPASS,
                set.ICONS_FOLDER_NAME,
                set.ICO_ICON_FILENAME
            )
        else:
            # If it runs as a python app
            icon_path_png = set.PNG_ICON_FILEPATH
            icon_path_ico = set.ICO_ICON_FILEPATH

        self.icon = ImageTk.PhotoImage(Image.open(icon_path_png))
        self.root.iconphoto(True, self.icon)
        self.root.iconbitmap(icon_path_ico)
