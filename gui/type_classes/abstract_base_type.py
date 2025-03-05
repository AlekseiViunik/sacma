import tkinter as tk
from abc import ABC, abstractmethod
from decimal import Decimal

from gui.widget_creator import WidgetCreator
from logic.json_file_handler import JsonFileHandler
from gui.helper import Helper
from settings import settings as set


class AbstractBaseType (ABC):
    """Базовый класс для всех типов элементов."""

    def __init__(self, root: tk.Tk, type: str) -> None:
        self.root = root
        self.type = type
        self.window = None  # Окно, которое будет создаваться при открытии
        self.type_choice = None   # Доступные варианты выбора типа
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

    def center_window(self, width: int, height: int, window=None) -> None:
        """Центрирует окно относительно экрана."""
        handled_window = window if window else self.window
        handled_window.update_idletasks()
        screen_width = handled_window.winfo_screenwidth()
        screen_height = handled_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        handled_window.geometry(f"{width}x{height}+{x}+{y}")

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

    def open_response_window(self, cost: Decimal, weight: Decimal) -> None:
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
        self.center_window(300, 150, result_window)  # Центрируем окно

        # Формируем текст для отображения
        prezzo_text = (
            f"{set.PRICE}: {cost} €" if cost else set.PRICE_NOT_FOUND
        )
        peso_text = (
            f"{set.WEIGHT}: {weight} Kg" if weight else set.WEIGHT_NOT_FOUND
        )

        # Выводим текст
        tk.Label(
            result_window,
            text=prezzo_text,
            font=("Arial", 12)
        ).pack(pady=5)
        tk.Label(
            result_window,
            text=peso_text,
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
