import importlib
import sys
from pathlib import Path
from typing import Tuple


class Helper:
    """Вспомогательный класс с утилитарными методами."""
    def __init__(self, root):
        self.root = root

    @staticmethod
    def get_type_class_name(name: str) -> Tuple[str]:
        """Преобразует строку в имя класса в CamelCase.

        Примеры:
        --------
            "this is a class" → "ThisIsAClass",
            "travi di battuta" → "TraviDiBattuta"

        Parameters
        ----------
            name : str
                Исходная строка.

        Returns
        -------
            str
                Строка в CamelCase (как имя класса).
        """
        class_file = "_".join(word.lower() for word in name.split())
        class_name = "".join(word.capitalize() for word in name.split())
        return class_name, class_file

    @staticmethod
    def get_class_name_if_exists(name):
        class_name, class_file = Helper.get_type_class_name(name)
        module_path = f"gui.type_classes.{class_file}"

        # ✅ Добавляем путь к `sys.path`, если его там нет
        type_classes_path = str(Path(__file__).parent / "type_classes")
        if type_classes_path not in sys.path:
            sys.path.append(type_classes_path)

        try:
            module = importlib.import_module(module_path)
            class_ = getattr(module, class_name)
            return class_
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Ошибка: {e}")  # Для отладки
            return False

    def on_close(self, window):
        window.destroy()
        self.root.deiconify()
