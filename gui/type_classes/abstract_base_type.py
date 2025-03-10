import tkinter as tk
from abc import ABC, abstractmethod

from gui.widget_creator import WidgetCreator
from logic.json_file_handler import JsonFileHandler
from logic.logger import logger as log
from gui.helper import Helper
from settings import settings as set


class AbstractBaseType (ABC):
    """
    Базовый класс для всех типов элементов.
    Содержит базовый функционал для создания окна для любого типа элементов,
    отображенных в виде кнопок на главном окне и имеющих свой класс,
    унаследованный от этого.


    Attributes
    ----------
    root : tk.Tk
        Главное окно.
    type : str | None
        Тип выбранного элемента (имя нажатой кнопки).
    entry_widgets : list
        Список виджетов с полем для ввода, которые рисуются в окне, если не
        передан type_choice
    window : tk.Toplevel
        Созданное окно для ввода данных элемента.
    type_choice : Dict
        Набор параметров для выбранного типа элементов.
    window_width : int
        Ширина созданного окна.
    window_height : int
        Высота созданного окна.
    entries : Dict
        Словарь с введенными значениями.
    json : JsonFileHandler
        Объект для работы с JSON-файлами.
    helper : Helper
        Объект для работы с вспомогательными методами.

    Methods
    -------
    open_window()
        Создает и центрирует новое окно с заголовком и базовыми компонентами.
    create_components()
        Создает и раскидывает компоненты окна.
    open_response_window(cost, weight)
        Открывает окно с результатом расчётов.
    calculate()
        Обработка нажатия кнопки. Для каждого класса своя. Должна быть
        переписана.
    """

    def __init__(
        self,
        root: tk.Tk,
        type: str | None = None,
        entry_widgets: list = None
    ) -> None:
        self.root = root
        self.type = type
        self.entry_widgets = entry_widgets
        self.window: tk.Toplevel = None
        self.type_choice: dict = None
        self.window_width: int = 0
        self.window_height: int = 0
        self.entries: tk.Entry = None
        self.json: JsonFileHandler = JsonFileHandler("options.json")
        self.helper: Helper = Helper(self.root)

    def open_window(
        self,
        title: str = "Title",
        window_width: int = 300,
        window_height: int = 300
    ) -> None:
        """
        Создаёт и центрирует новое окно с заголовком и базовыми компонентами.
        Вызывает метод создания компонентов.

        Parameters
        ----------
        title : str
            Имя окна
        window_width : int
            Ширина окна
        window_height : int
            Высота окна
        """
        log.info(f"Opening window '{title}'")
        self.root.withdraw()
        self.window = tk.Toplevel(self.root)
        if self.type:
            self.type_choice = self.json.read_value_by_key(self.type.lower())
            self.window.title(self.type.capitalize())
            self.window_width = self.type_choice['window_settings']['width']
            self.window_height = self.type_choice['window_settings']['height']
        else:
            self.type_choice = None
            self.window.title = title
            self.window_width = window_width
            self.window_height = window_height

        geometry = f"{self.window_width}x{self.window_height}"
        self.window.geometry(geometry)
        Helper.center_window(
            self.window_width,
            self.window_height,
            self.window
        )
        log.info("Widow is opened. Create components")
        self.create_components()

    def create_components(self) -> None:
        """
        Создаёт компоненты окна. Использует Widget creator для размещения
        виджетов и кнопки. Перезаписывает свойство класса entries.
        """

        creator = WidgetCreator(
            self.window,
            self.type_choice
        )
        if self.type_choice:
            log.info("Create always_on widgets")
            row = creator.create_always_on()
            log.info("Create main frame")
            creator.create_main_frame(row)
            log.info("Create 'Invia' button")
            creator.create_button("Invia", self.calculate)

        else:
            frame = creator.create_frame(self.window.title)
            for i, label in enumerate(self.entry_widgets):
                creator.create_component(
                    frame,
                    label,
                    [],
                    i,
                    is_entry=True,
                    is_hide=True if "password" in label.lower() else False
                )
            for i in range(set.COL_NUM):
                frame.columnconfigure(i, weight=set.GRID_WEIGHT)
            creator.create_button("Creare", self.calculate)

        self.entries = creator.entries

        self.window.protocol(
            set.ON_CLOSING_WINDOW,
            lambda: Helper(self.root).on_close(self.window)
        )
        log.info("Components are created!")

    def open_response_window(self, data: dict, warning=None) -> None:
        """
        Открывает окно с результатом расчётов.
        Parameters
        ----------
        data : dict
            Результат расчёта цены и веса. Допускает и другие значения.
        """

        # Открываем окно
        log.info("Open response window")
        result_window = tk.Toplevel(self.root)
        result_window.title("Risultato")  # Заголовок окна
        Helper.center_window(300, 150, result_window)  # Центрируем окно

        for key, value in data.items():
            if key == "price":
                text = (
                    f"{set.PRICE}: {value} €" if value else set.PRICE_NOT_FOUND
                )
            elif key == "weight":
                text = (
                    f"{set.WEIGHT}: {value} Kg"
                    if value else set.WEIGHT_NOT_FOUND
                )
            else:
                text = f"{key}: {value}" if value else "NOT FOUND"

            # Выводим текст
            tk.Label(
                result_window,
                text=text,
                font=("Arial", 12)
            ).pack(pady=5)
            log.info(f"Text is {text}")
        if warning:
            Helper.center_window(450, 200, result_window)
            tk.Label(
                result_window,
                text=warning,
                font=("Arial", 12)
            ).pack(pady=5)
            log.info(f"Warning text is {warning}")

        # Кнопка "OK", которая закроет окно
        tk.Button(
            result_window,
            width=set.BUTTON_WIDTH,
            bg=set.BUTTON_COLOR,
            text="OK",
            command=result_window.destroy
        ).pack(pady=10)

    @abstractmethod
    def calculate(self) -> None:
        """
        Выполнение действия при нажатии на кнопку. Для каждого класса свое.
        """
        pass
