from abc import ABC, abstractmethod
import tkinter as tk


class AbstractTypeClass(ABC):
    """Абстрактный класс для всех типов элементов."""

    def __init__(self, root: tk.Tk, name) -> None:
        """Инициализация базовых свойств."""
        self.root = root
        self.name = name
        self.window = None  # Окно, которое будет создаваться при открытии
        self.type_choice: dict = {}  # Доступные варианты выбора типа
        self.window_width = 0
        self.window_height = 0
        self.entries = None

    def open_window(self) -> None:
        """Создаёт новое окно с заголовком и базовыми компонентами."""
        self.window = tk.Toplevel(self.root)
        self.window.title(self.window_title)
        self.window.geometry("400x300")  # Пока такой размер, можно менять

        # Центрируем окно
        self.center_window(400, 300)

    @abstractmethod
    def calculate(self) -> None:
        pass

    @abstractmethod
    def open_response_window(self, cost: float, weight: float) -> None:
        """Абстрактный метод: открывает окно с ответом после расчёта."""
        pass

    def center_window(self, width: int, height: int, window=None) -> None:
        """Центрирует окно относительно экрана."""
        handled_window = window if window else self.window
        handled_window.update_idletasks()
        screen_width = handled_window.winfo_screenwidth()
        screen_height = handled_window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        handled_window.geometry(f"{width}x{height}+{x}+{y}")
