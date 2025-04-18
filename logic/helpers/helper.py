import re

from datetime import datetime
from decimal import Decimal
from numbers import Number
from typing import Any

from settings import settings as sett


class Helper:
    """
    Главный помощник. Собрал в себе различные методы, которые я не знаю, куда
    деть.

    Methods
    -------
    - get_nested_data(keys, data)
        Ищет в многоуровневом словаре значение по ключам.

    - merge_numeric_dicts(dict1, dict2)
        Объединяет 2 словаря в один, беря из обоих только значения, которые
        могут стать в итоге числами.

    - backward_convertation(value, convertation_dictionary)
        Конвертирует значения в исходные в соответствии со словарем
        конвертации.

    - get_current_time()
        Возвращает текущую дату и время в формате "YYYY-MM-DD HH:MM:SS".
    """

    @staticmethod
    def get_nested_data(keys: list, data: dict) -> dict | None:
        """
        Рекурсивно ищет значение в многоуровневом словаре `data`, используя
        ключи из `keys`, независимо от их порядка.
        Ищет по принципу: нашел хоть какой-то ключ из списка - перешел на
        уровень глубже и снова ищет хоть какой-то ключ из оставшихся ключей из
        списка. И так далее, пока не переберет все ключи или пока из оставшихся
        ключей ни один не будет найден на текущем уровне.

        Частный случай: перед поиском ключей на текущем уровне словаря, если в
        словаре есть ключ `choice`, то перескакивает на 2 уровня глубже. А если
        еще и `cells_output` в словаре по ключу `choice`, то возвращаем этот
        словарь.

        Parameters
        ----------
        - keys: list
            Массив ключей, по которым надо искать вложенные словари.

        - data: dict
            Многоуровневый словарь, по которому будет вестись поиск.

        Returns
        -------
        - data: dict | None
            Найденный по всем переданным ключам словарь.
        """

        # Если нашли ключ.
        if data.get(sett.CHOICES) and data[sett.CHOICES].get(
            sett.CELLS_OUTPUT
        ):
            return data[sett.CHOICES]

        counter = sett.SET_TO_ZERO

        # Пробегаемся по ключам.
        for key in keys:

            # Если ключ - "choices", перескакиваем на 2 уровня.
            if sett.CHOICES in data and key in data[sett.CHOICES]:
                return Helper.get_nested_data(
                    [k for k in keys if k != key], data[sett.CHOICES][key]
                )  # Удаляем найденный ключ и продолжаем.

            # В противном случае переходим на следующий уровень вложенности.
            elif key in data:
                return Helper.get_nested_data(
                    [k for k in keys if k != key], data[key]
                )  # Удаляем найденный ключ и продолжаем.
            else:
                counter += sett.STEP_UP

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

        Parameters
        ----------
        - dict1: dict
            Первый словарь для объединения.
        - dict2: dict
            Второй словарь для объединения.

        Returns
        -------
        - _: dict
            Объединенный словарь с преобразованными в Decimal значение.
        """
        def to_decimal(value: Any) -> Decimal | None:
            """
            Преобразует числовое значение (или строку с числом) в Decimal.

            Parameters
            ----------
            - value: Any
                Значение для преобразования.
            Returns
            -------
            - _: Decimal | None
                Преобразованное значение. Если тип не поддерживаемый, то
                возвращает None.
            """

            # Числовой тип (int, float, Decimal)
            if isinstance(value, Number):
                return Decimal(value)

            # Ищем число в строке (поддержка "." и "," в десятичной части)
            if isinstance(value, str):

                # Регулярка  для поиска цифр + разделителя
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

    @staticmethod
    def backward_convertation(
        value: str,
        convertation_dictionary: dict
    ) -> str:
        """
        Ищет значения среди значений словаря конвертации и возвращает ключ.

        Parameters
        ----------
        - value: str
            Значение, которое нужно конвертировать.
        - convertation_dictionary: dict
            Словарь конвертации, где ключ - это название, а значение - его
            конвертированное значение.

        Returns
        -------
        - _: str
            Название, соответствующее переданному значению.
        """

        for key, val in convertation_dictionary.items():
            if val == value:
                return key
        return ""

    @staticmethod
    def get_current_time() -> str:
        """
        Возвращает текущую дату и время в формате "YYYY-MM-DD HH:MM:SS".

        Returns
        -------
        - _: str
            Текущая дата и время.
        """
        return datetime.now().strftime(
            sett.DATE_TIME_FORMAT
        )
