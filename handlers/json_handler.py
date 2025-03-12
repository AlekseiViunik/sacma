import json
import os

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
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    key: field.text()
                    for key, field in data.items()
                },
                f, indent=4, ensure_ascii=False
            )
