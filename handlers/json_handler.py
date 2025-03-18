import json
import os

from PyQt6.QtWidgets import QLineEdit

from typing import Any


class JsonHandler:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path if os.path.exists(file_path) else None

    def get_all_data(self) -> dict:
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

    def get_value_by_key(self, key: str) -> Any:
        data = self.get_all_data()
        if data:
            return data.get(key, "")
        return ""

    def get_values_by_keys(self, keys: list) -> dict:
        """
        Возвращает словарь со значениями для переданных ключей, найденными в
        json файле.

        Параметры
        ---------
        keys : list
            список ключей, для которых нужно найти значения в файле.

        Возвращает
        ----------
        result : dict
            Словарь со значениями для этих ключей. Или пустой словарь.
        """
        result = {}
        data = self.get_all_data()

        if data:
            for key in keys:
                if key in data.keys():
                    result[key] = data.get(key, "")

        return result

    def rewrite_file(self, data: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    key: field.text() if isinstance(field, QLineEdit)
                    else field for key, field in data.items()
                },
                f, indent=4, ensure_ascii=False
            )

    def write_into_file(self, key="", key2="", value="") -> None:
        """
        Записывает данные в файл.

        Parameters
        ----------
        key : str
            Ключ первого уровня для записи.
        key2 : str | None
            Ключ второго уровня
        value: str
            Значение, которое нужно записать.
        """
        data = self.get_all_data()
        if not key2:
            data[key] = value
        else:
            data[key][key2] = value
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
