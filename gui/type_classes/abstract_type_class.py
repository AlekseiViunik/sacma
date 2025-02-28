from abc import ABC, abstractmethod
import tkinter as tk


class AbstractTypeClass(ABC):
    """Абстрактный класс для всех типов элементов."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализация базовых свойств."""
        self.root = root
        self.window = None  # Окно, которое будет создаваться при открытии
        self.window_title: str = ""  # Заголовок окна (задаётся в наследниках)
        self.type_choices: dict = {}  # Доступные варианты выбора типа

    def open_window(self) -> None:
        """Создаёт новое окно с заголовком и базовыми компонентами."""
        self.window = tk.Toplevel(self.root)
        self.window.title(self.window_title)
        self.window.geometry("400x300")  # Пока такой размер, можно менять

        # Центрируем окно
        self.center_window(400, 300)

    @abstractmethod
    def put_data_in_excel(self) -> None:
        """Абстрактный метод: вставляет данные в Excel."""
        pass

    @abstractmethod
    def get_data_from_excel(self) -> None:
        """Абстрактный метод: получает данные из Excel."""
        pass

    @abstractmethod
    def open_response_window(self, cost: float, weight: float) -> None:
        """Абстрактный метод: открывает окно с ответом после расчёта."""
        pass

    def center_window(self, width: int, height: int) -> None:
        """Центрирует окно относительно экрана."""
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
