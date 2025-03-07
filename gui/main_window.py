import math
import tkinter as tk

from gui.create_user_window import CreateUserWindow
from gui.widget_creator import WidgetCreator

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
        self.creator = WidgetCreator(self.root)
        Helper.center_window(
            set.MAIN_WIN_WIDTH,
            set.MAIN_WIN_HEIGHT,
            self.root
        )

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

        self.creator.create_button(
            "Create user",
            self.open_create_user_window,
            "s"
        )

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

    def open_create_user_window(self):
        create_user = CreateUserWindow(
            self.root,
            entry_widgets=set.CREATE_USER_ENTRIES
        )
        create_user.open_window()
