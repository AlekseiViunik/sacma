import math
import tkinter as tk

from gui.create_user_window import CreateUserWindow
from gui.helper import Helper
from gui.widget_creator import WidgetCreator
from logic.logger import logger as log
from settings import settings as set


class App:
    """
    Класс App используется для создания основного окна.

    Основное применение - создание главного окна приложения и его кнопок,
    Запус процесса обработки входных данных и вывод результата в отдельном
    окне. Во время инициализации сразу же вызывает метод раскидывания виджетов
    по окну.

    Attributes
    ----------
    root : tk.Tk
        Главное окно.
    entries : dict
        список введенных значений.
    buttons : list
        список кнопок, размещаемых на главном окне.
    creator : WidgetCreator
        объект класса WidgetCreator ответственного за создание и размещение
        виджетов

    Methods (все приватные)
    -------
    __create_widgets()
        Раскидывает виджеты по главному окну.
    __open_window(name)
        Открывает второстепенное окно с базовыми виджетами, одинаковыми для
        всех такого рода окон.
    __open_create_user_window()
        Открывает окно создание юзеров, которое отличается от других окон.
    __check_if_class_exists(name)
        Проверяет, существует ли класс с названием кнопки.
    """
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.resizable(False, False)
        self.entries: dict = {}
        self.root.title(f"{set.MAIN_WIN_TITLE}")
        self.root.geometry(f"{set.MAIN_WIN_WIDTH}x{set.MAIN_WIN_HEIGHT}")
        self.buttons: list = set.MAIN_WIN_BUTTONS
        self.creator = WidgetCreator(self.root)
        Helper.center_window(
            set.MAIN_WIN_WIDTH,
            set.MAIN_WIN_HEIGHT,
            self.root
        )

        self.__create_widgets()

# ============================== Приватные методы =============================

    def __create_widgets(self) -> None:
        """
        Создает виджеты для главного окна. Сами виджеты подразумевают под
        собой фреймы, кнопки, лейблы. Вызывать не надо - вызывается
        автоматически.
        """

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
                state=(
                    tk.NORMAL
                    if self.__check_if_class_exists(name)
                    else tk.DISABLED
                ),
                command=lambda n=name: self.__open_window(n)
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
            self.__open_create_user_window,
            "s"
        )

        log.info("Widgets are created")

    def __check_if_class_exists(self, name: str) -> object | bool:
        """
        Проверяет, существует ли класс. Если существует, возвращает его.
        В противном случае возвращает False.

        Parameters
        ----------
        name : str
            Имя кнопки/класса

        Returns
        -------
        object | bool
            Возвращает объект класса или False, если класс не найден
        """
        log.info(f"Check if {name} class exists")
        class_name = Helper.get_class_name_if_exists(name)
        return class_name(self.root, name) if class_name else False

    def __open_create_user_window(self) -> None:
        """
        Создает окно с полями для ввода логина и пароля нового пользователя.
        """

        log.info("Open user creation window")
        create_user = CreateUserWindow(
            self.root,
            entry_widgets=set.CREATE_USER_ENTRIES
        )
        create_user.open_window()

    def __open_window(self, name: str) -> None:
        """
        Открывает базу второстепенного окна фреймом и кнопкой Invia.
        В зависимости от того, какая кнопка была нажата, вызывает частный
        вспомогательный метод для отрисовки компонентов. Будет работать,
        только если существует модуль с классом, имя которого совпадает с
        переданным в параметры именем.

        Parameters
        ----------
            name: str
                Имя окна. От него же зависит начинка окна виджетами.
        """
        log.info(f"Trying to open window {name}")
        instance = self.__check_if_class_exists(name)
        if instance:
            log.info(f"Class {name} is found. Openning the window.")
            instance.open_window()
        else:
            log.error(f"Class {instance} not found!")
