import importlib
import tkinter as tk
import sys

from pathlib import Path


class Helper:
    """
    Вспомогательный класс с утилитарными методами.

    Attributes
    ----------
    root : tk.Tk
        Главное окно

    Methods
    -------
    on_close(window)
        Обрабатывает закрытие окна.
    get_type_class_name(name)
        Преобразует строку в имя класса в CamelCase и имя модуля класса.
    get_class_name_if_exists(name, path)
        Проверяет, существует ли класс с переданным именем.
    center_window()
        Центрирует окно на экране.
    """

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

    def on_close(self, window: tk.Toplevel) -> None:
        """
        Обрабатывает закрытие окна. Когда окно закрывается, то главное окно,
        которое было скрыто, снова становится видимым.

        Parameters
        ----------
        window : tk.Toplevel
            Окно, которое нужно закрыть.
        """
        window.destroy()
        self.root.deiconify()

    @staticmethod
    def get_type_class_name(name: str) -> tuple:
        """
        Преобразует строку в имя класса в CamelCase.
        Также преобразует ту же строку в имя файла в snake_case.

        Примеры:
        --------
        "this is a class" → "ThisIsAClass" и "this_is_a_class",
        "travi di battuta" → "TraviDiBattuta" и "travi_di_battuta".

        Parameters
        ----------
        name : str
            Исходная строка.

        Returns
        -------
        tuple
            Кортеж из одной строки в CamelCase (как имя класса) и второй в
            snake_case (как имя файла).
        """
        class_file = "_".join(word.lower() for word in name.split())
        class_name = "".join(word.capitalize() for word in name.split())
        return class_name, class_file

    @staticmethod
    def get_class_name_if_exists(name: str, path="") -> bool | type:
        """
        Проверяет, существует ли класс с переданным именем. Если существует,
        то возвращает его, иначе возвращает False. Проверка осуществляется
        путем попытки импортировать модуль файла с классом и получения имени
        класса из этого модуля. Если модуль не найден или в нём нет класса
        с переданным именем, то возвращается False.
        Если path не передан, использует стандартный.

        Parameters
        ----------
        name : str
            Имя предполагаемого класса.

        Returns
        -------
        bool | type
            Возвращает класс, если он существует, иначе возвращает False.

        """
        class_name, class_file = Helper.get_type_class_name(name)
        module_path = f"gui.type_classes.{class_file}" if not path else path

        # ✅ Добавляем путь к `sys.path`, если его там нет
        type_classes_path = str(Path(__file__).parent / "type_classes")
        if type_classes_path not in sys.path:
            sys.path.append(type_classes_path)

        try:
            module = importlib.import_module(module_path)
            class_ = getattr(module, class_name)
            return class_
        except (ModuleNotFoundError, AttributeError):
            return False

    @staticmethod
    def center_window(
        width: int,
        height: int,
        window: tk.Toplevel | tk.Tk
    ) -> None:
        """
        Центрирует окно относительно экрана компьютера. Основываясь на размерах
        самого окна. Меняет при этом размеры самого окна

        Parameters
        ----------
        width : int
            Ширина окна
        Height : int
            Высота окна
        window : tk.Toplevel
            Окно, которое необходимо центрировать
        """

        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
