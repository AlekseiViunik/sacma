import json
from typing import Any

from logic.logger import logger as log


class JsonFileHandler:
    """
    Класс JsonFileHandler используется для работы с JSON-файлами.

    Attributes
    ----------
    file : str
        Путь к JSON-файлу или имя файла, если он лежит в корне проекта.

    Methods
    -------
    read_value_by_key(key: str) -> Any
        Читает JSON и возвращает значение по переданному ключу.
    """

    def __init__(self, file: str):
        self.file = file

    def read_value_by_key(self, key: str) -> Any:
        """
        Читает JSON и возвращает значение по переданному ключу.

        Parameters
        ----------
        key : str
            Ключ, по которому нужно вернуть значение из файла.

        Returns
        -------
        Any
            Возвращает значение по ключу или None, если ключ не найден.
        """
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)  # Загружаем JSON в словарь

            return data.get(key, None)  # Возвращаем значение по ключу или None

        except FileNotFoundError:
            log.error(f"❌ Файл '{self.file}' не найден.")
            return None
        except json.JSONDecodeError:
            log.error(f"❌ Ошибка чтения JSON в файле '{self.file}'.")
            return None
