import tkinter as tk
from abc import ABC, abstractmethod
from typing import Any, Dict

from gui.widget_creator import WidgetCreator
from logic.json_file_handler import JsonFileHandler
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
    type : str
        Тип выбранного элемента (имя нажатой кнопки).
    window : tk.Toplevel
        Созданное окно для ввода данных элемента.
    type_choice : Dict
        Набор параметров для выбранного типа элементов.
    window_width : int
        Ширина созданного окна.
    window_height : int
        Высота созданного окна.
    entries : Dict
        Список введенных значений.
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
        Расчёт стоимости и веса. Для каждого класса свой.
    """

    def __init__(self, root: tk.Tk, type: str) -> None:
        self.root = root
        self.type = type
        self.window: tk.Toplevel = None
        self.type_choice: Dict[str, Any] = None
        self.window_width: int = 0
        self.window_height: int = 0
        self.entries: tk.Entry = None
        self.json: JsonFileHandler = JsonFileHandler("options.json")
        self.helper: Helper = Helper(self.root)

    def open_window(self) -> None:
        """
        Создаёт и центрирует новое окно с заголовком и базовыми компонентами.
        Вызывает метод создания компонентов.
        """
        self.type_choice = self.json.read_value_by_key(self.type.lower())
        self.root.withdraw()
        self.window = tk.Toplevel(self.root)
        self.window.title(self.type.capitalize())
        self.window_width = self.type_choice['window_settings']['width']
        self.window_height = self.type_choice['window_settings']['height']
        geometry = f"{self.window_width}x{self.window_height}"
        self.window.geometry(geometry)
        Helper.center_window(
            self.window_width,
            self.window_height,
            self.window
        )
        self.create_components()

    def create_components(self) -> None:
        """Создаёт компоненты окна. Использует Widget creator для размещения
        виджетов и кнопки Invia. Перезаписывает свойство класса entries."""
        creator = WidgetCreator(
            self.window,
            self.type_choice
        )
        creator.create_ui()
        self.entries = creator.entries

        creator.create_invia_button(self.calculate)

        self.window.protocol(
            set.ON_CLOSING_WINDOW,
            lambda: Helper(self.root).on_close(self.window)
        )

    def open_response_window(self, data: dict) -> None:
        """
        Открывает окно с результатом расчётов.
        Parameters
        ----------
        cost : Decimal
            Результат расчёта цены.
        weight : Decimal
            Результат расчёта веса.
        """

        # Открываем окно
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
                text = f"{key}: {value}" if value else "NOT_FOUND"

            # Выводим текст
            tk.Label(
                result_window,
                text=text,
                font=("Arial", 12)
            ).pack(pady=5)

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
        """Расчёт стоимости и веса. Для каждого класса свой."""
        pass
