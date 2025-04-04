import json
import os
import sys

from PyQt6.QtWidgets import QLineEdit
from typing import Any

from interface.windows.messagebox import Messagebox
from logic.logger import logger as log
from settings import settings as sett


class JsonHandler:
    """
    Обработчик файлов JSON. Служит для получения/записи данных в эти файлы.

    Attributes
    ----------
    - file_path: str
        Путь к файлу JSON

    Methods
    -------
    - get_all_data()
        Получает все данные из файла и преобразует их в словарь.

    - get_value_by_key(key)
        Получает данные из файла по ключу.

    - get_values_by_keys(keys)
        Получает данные из файла по списку ключей.

    - rewrite_file(data)
        Полностью перезаписывает файл новыми данными.

    - write_into_file(key, key2, value)
        Перезаписывает отдельное значение файла. Работает до ключей второго
        уровня глубины включительно.

    - set_file_path(path)
        Этот метод нужен, чтобы настроить абсолютный путь к файлу, если
        приложение работает как ехе файл.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path: str = sett.EMPTY_STRING

        self.set_file_path(file_path)

    def get_all_data(self) -> dict:
        """
        Открывает JSON файл только для чтения, получает все данные и возвращает
        их в виде словаря.

        Returns
        -------
        - _: dict
            Возвращаемые данные.
        """
        log.info(sett.JSON_GET_ALL_DATA)
        if self.file_path:
            try:
                with open(
                    self.file_path,
                    sett.FILE_READ,
                    encoding=sett.STR_CODING
                ) as f:
                    return json.load(f)
            except FileNotFoundError:
                Messagebox.show_messagebox(
                    sett.FILE_NOT_FOUND,
                    sett.FNF_MESSAGE,
                    None,
                    exec=True
                )
                raise FileNotFoundError(
                    sett.FNF_MESSAGE
                )

    def get_value_by_key(self, key: str) -> Any:
        """
        Открывает JSON файл только для чтения, получает данные по ключу и
        возвращает их в том виде, в котором они там хранятся.

        Parameters
        ----------
        - key: str
            Ключ, по которому надо получить данные.

        Returns
        -------
        - _: Any
            Возвращаемые данные.
        """
        log.info(sett.JSON_GET_VALUE_BY_KEY)
        data = self.get_all_data()
        if data:
            return data.get(key, sett.EMPTY_STRING)
        return sett.EMPTY_STRING

    def get_values_by_keys(self, keys: list) -> dict:
        """
        Открывает JSON файл только для чтения, получает данные по списку
        ключей и возвращает их в виде словаря, где ключами будут те самые
        переданные в списке ключи.

        Parameters
        ----------
        - keys : list
            список ключей, для которых нужно найти значения в файле.

        Returns
        -------
        - result : dict
            Словарь со значениями для этих ключей. Или пустой словарь.
        """
        log.info(sett.JSON_GET_VALUES_BY_KEYS)
        result = {}
        data = self.get_all_data()

        if data:
            for key in keys:
                if key in data.keys():
                    result[key] = data.get(key, sett.EMPTY_STRING)

        return result

    def rewrite_file(self, data: dict) -> None:
        """
        Открывает файл JSON для записи и полностью перезаписывает его, заменяя
        имеющиеся там данные переданными в метод. Обычно используется для
        одноуровневого словаря.

        Parameters
        ----------
        - data: dict
            Данные, которыми будет перезаписан файл.
        """
        log.info(sett.JSON_REWRITE_FILE)
        with open(
            self.file_path,
            sett.FILE_WRITE,
            encoding=sett.STR_CODING
        ) as f:
            json.dump(
                {
                    # Иногда в качестве значений может быть объект QLineEdit, а
                    # нам нужно введенное в это поле значение. В таком случае
                    # Передаем в создаваемый словарь его значение. В остальных
                    # случаях передаем непреобразованное значение.
                    key: field.text()
                    if isinstance(field, QLineEdit)
                    else field
                    for key, field in data.items()
                },
                f, indent=4, ensure_ascii=False
            )

    def write_into_file(
        self,
        key: str = sett.EMPTY_STRING,
        key2: str = sett.EMPTY_STRING,
        value: str | dict = sett.EMPTY_STRING
    ) -> None:
        """
        Открывает файл JSON для записи, получает из него все данные,
        меняет значение данных по ключам (поддержка до второго уровня
        вложенности словарей) и полностью перезаписывает файл с уже измененным
        словарем.

        Parameters
        ----------
        - key : str
            Ключ первого уровня для записи.
        - key2 : str
            Ключ второго уровня
        - value: str | dict
            Значение, которое нужно записать.
        """

        log.info(sett.JSON_WRITE_INTO_FILE)
        data = self.get_all_data()
        if not key2:
            data[key] = value
        else:
            data[key][key2] = value
        self.rewrite_file(data)

    def set_file_path(self, path: str) -> None:
        """
        Устанавливает абсолютный путь к файлу, если приложение работает как ехе
        файл.

        Parameters
        ----------
         - path: str
            относительный путь к файлу.
        """
        if getattr(sys, sett.EXE_FROZEN, False):
            BASE_DIR = os.path.dirname(sys.executable)
            self.file_path = os.path.join(BASE_DIR, path)
        else:
            self.file_path = path
