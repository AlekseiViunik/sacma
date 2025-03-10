import json

from typing import Any

from logic.logger import logger as log
from settings import settings as set


class JsonFileHandler:
    """
    Класс JsonFileHandler используется для работы с JSON-файлами.

    Attributes
    ----------
    file : str
        Путь к JSON-файлу или имя файла, если он лежит в корне проекта.

    Methods
    -------
    read_value_by_key(key: str)
        Читает JSON и возвращает значение по переданному ключу.
    load_whole_file()
        Возвращает файл целиком
    write_into_file(key, key2, value)
        Записывает данные в файл
    """

    def __init__(self, file: str):
        self.file = file

    def read_value_by_key(self, key: str) -> Any | None:
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

    def load_whole_file(self) -> json:
        """
        Возвращает все данные файла.

        Returns
        -------
        json
            Данные файла.
        """
        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

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
        data = self.load_whole_file()
        if not key2:
            data[key] = value
        else:
            data[key][key2] = value
        with open(set.AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
