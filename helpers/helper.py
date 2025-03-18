import re
from decimal import Decimal
from numbers import Number
from PyQt6.QtWidgets import QApplication, QWidget


class Helper:

    @staticmethod
    def move_window_to_center(window: QWidget):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - window.window_width) // 2
        y = (screen_geometry.height() - window.window_height) // 2
        window.setGeometry(x, y, window.window_width, window.window_height)

    @staticmethod
    def move_window_to_top_left_corner(window: QWidget):
        window.setGeometry(40, 50, window.window_width, window.window_height)

    @staticmethod
    def get_calculation_file(name: str) -> str:
        filename = "_".join(word.lower() for word in name.split())
        return f"configs/calculator_configs/{filename}.json"

    @staticmethod
    def get_nested_data(keys: list, data: dict) -> dict | None:
        """Рекурсивно ищет значение в словаре `data`, используя ключи из `keys,
        независимо от их порядка."""

        if data.get('choices') and data['choices'].get('cells_output'):
            return data['choices']

        counter = 0
        for key in keys:
            if "choices" in data and key in data["choices"]:
                return Helper.get_nested_data(
                    [k for k in keys if k != key], data["choices"][key]
                )  # Удаляем найденный ключ и продолжаем
            elif key in data:
                return Helper.get_nested_data(
                    [k for k in keys if k != key], data[key]
                )  # Удаляем найденный ключ и продолжаем
            else:
                counter += 1

        if counter == len(keys):
            return data

        return None

    @staticmethod
    def merge_numeric_dicts(dict1: dict, dict2: dict) -> dict:
        """
        Объединяет два словаря, оставляя только числовые значения (включая
        строки с числами).
        - Преобразует числа (в т.ч. строки с числами) в `Decimal`.
        - Игнорирует строки, содержащие текст, булевы значения и другие типы.
        """
        def to_decimal(value):
            """Преобразует числовое значение (или строку с числом) в Decimal"""
            if isinstance(value, Number):  # Числовой тип (int, float, Decimal)
                return Decimal(value)

            if isinstance(value, str):
                # Ищем число в строке (поддержка точек и запятых в десятичной
                # части)
                match = re.search(r"\d+([.,]\d+)?", value)
                if match:
                    # Меняем запятую на точку
                    num_str = match.group().replace(",", ".")
                    return Decimal(num_str)
            return None  # Если значение не подходит, пропускаем

        return {
            k: dec_value for d in (dict1, dict2) for k, v in d.items()
            if (dec_value := to_decimal(v)) is not None
        }
