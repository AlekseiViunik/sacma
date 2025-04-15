import json
import os
import shutil
import sys

from PyQt6.QtWidgets import QLineEdit
from typing import Any

from interface.windows.messagebox import Messagebox
from logic.helpers.helper import Helper
from logic.protectors.encoder import Encoder
from logic.logger import logger as log
from logic.protectors.config_protector import ConfigProtector
from settings import settings as sett


class JsonHandler:
    """
    Обработчик файлов JSON. Служит для получения/записи данных в эти файлы.

    Attributes
    ----------
    - file_path: str
        Путь к файлу JSON

    - is_encoded: bool
        Default = False\n
        Флаг, указывающий, закодирован ли файл.

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

    def __init__(self, file_path: str, is_encoded: bool = False) -> None:
        self.file_path: str = sett.EMPTY_STRING
        self.is_encoded: bool = is_encoded
        self.encoder = Encoder()

        self.set_file_path(file_path)

    def get_all_data(self) -> dict:
        """
        Открывает JSON файл только для чтения, получает все данные и возвращает
        их в виде словаря. Расшифровывает, если требуется.

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
                    data = json.load(f)
                    if self.is_encoded:
                        # Если файл закодирован, то сначала его нужно
                        # расшифровать.
                        data = self.encoder.decrypt_data(data)
                if isinstance(data, list):
                    # Если данные в файле - это список, то преобразуем его в
                    # словарь.
                    return data[sett.SET_TO_ZERO]
                return data

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

        ConfigProtector.unset_read_only(self.file_path)

        log.info(sett.JSON_REWRITE_FILE)
        with open(
            self.file_path,
            sett.FILE_WRITE,
            encoding=sett.STR_CODING
        ) as f:
            data = {
                # Иногда в качестве значений может быть объект QLineEdit, а
                # нам нужно введенное в это поле значение. В таком случае
                # Передаем в создаваемый словарь его значение. В остальных
                # случаях передаем непреобразованное значение.
                key: field.text()
                if isinstance(field, QLineEdit)
                else field
                for key, field in data.items()
            }
            if self.is_encoded:
                # Если файл закодирован, то сначала его нужно
                # зашифровать.
                try:
                    data = self.encoder.encrypt_data(data)
                except Exception as e:
                    Helper.log_exception(e)

            json.dump(
                data, f, indent=sett.INDENT, ensure_ascii=False
            )

        if sett.PRODUCTION_MODE_ON:
            ConfigProtector.set_read_only(self.file_path)

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
        словарем. Шифрует, если требуется.

        Parameters
        ----------
        - key : str
            Default = ''\n
            Ключ первого уровня для записи.
        - key2 : str
            Default = ''\n
            Ключ второго уровня
        - value: str | dict
            Default = ''\n
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

    def create_file_if_not_exists(self) -> None:
        """
        Если файл не существует, то создает его и копирует туда файл
        настроек по умолчанию. Если не получается, то выводит сообщение об
        ошибке.
        """

        if not os.path.exists(self.file_path):
            try:
                os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
                shutil.copy(sett.SETTINGS_FILE, self.file_path)
                log.info(
                    sett.USER_SETTINGS_FILE_CREATED.format(
                        self.file_path
                    )
                )
            except Exception as e:
                Helper.log_exception(e)
                Messagebox.show_messagebox(
                    sett.FAILED_TO_CREATE_FILE,
                    sett.COULDNT_CREATE_FILE.format(e),
                    None,
                    exec=True
                )
