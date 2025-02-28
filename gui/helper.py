import importlib
from typing import Tuple


class Helper:
    """Вспомогательный класс с утилитарными методами."""

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

        try:
            module = importlib.import_module(module_path)
            class_ = getattr(module, class_name)
            return class_
        except (ModuleNotFoundError, AttributeError):
            return False
