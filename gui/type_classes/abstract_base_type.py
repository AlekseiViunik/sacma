import tkinter as tk
from abc import ABC, abstractmethod
from typing import Dict, List

from logic.json_file_handler import JsonFileHandler
from gui.helper import Helper


class AbstractBaseType (ABC):
    """Базовый класс для всех типов элементов."""

    def __init__(self, root: tk.Tk, type: str) -> None:
        """Инициализация базовых свойств."""
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
        """Создаёт новое окно с заголовком и базовыми компонентами."""
        self.type_choice = self.json.read_value_by_key(self.type.lower())
        self.root.withdraw()
        self.window = tk.Toplevel(self.root)
        self.window.title(self.type.capitalize())
        self.window_width = self.type_choice['window_settings']['width']
        self.window_height = self.type_choice['window_settings']['height']
        geometry = f"{self.window_width}x{self.window_height}"
        self.window.geometry(geometry)
        self.center_window(self.window_width, self.window_height)
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

    def get_default_options(
        self,
        default_choice: str,
        option: str
    ) -> Dict[str, List[str]]:
        if (option == "alwais_on"):
            return (self.type_choice[option])
        return (
            self.type_choice[
                "choices"
            ][default_choice]["available_params"][option]
        )

    @abstractmethod
    def create_components(self) -> None:
        pass

    @abstractmethod
    def calculate(self) -> None:
        pass
