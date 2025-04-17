import re

from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from logic.helpers.translator import Translator
from logic.helpers.validator import Validator
from settings import settings as sett


class DataPreparator:
    """
    Класс для подготовки данных перед записью в Excel или после их извлечения
    оттуда.

    Attributes
    ----------
    - data : dict[str, str | Any]
        Default = {}\n
        Словарь с данными, которые нужно подготовить.

    - rules : dict
        Default = {}\n
        Словарь с правилами валидации данных.

    Methods
    -------
    - prepare_data(cells_input)
        Подготавливает данные (см. описание метода) перед вставкой их в эксель.

    - check_data()
        Валидирует входные данные согласно правилам изложенным в конфиге окна.

    - decimalize_and_rounding(self, excel_data, roundings)
        Переводит в Децимал и округляет значения по заданным параметрам или
        по умолчанию.

    Private Methods
    ---------------
    - __set_err_msg(rule_key, rule_value, key, value)
        В случае проваленной валидации данных, формирует сообщение об ошибке в
        зависимости от того, какое правило было провалено.
    """

    def __init__(
        self,
        data: dict[str, str | Any] = {},
        rules: dict = {}
    ) -> None:
        self.data = data
        self.rules = rules

    def prepare_data(self, cells_input: dict) -> dict:
        """
        В имеющемся эксель файлe есть варианты <1000 и >1001. Это не совсем
        логично, поэтому я заменил эти варианты для выбора пользователем на
        более логичные <=1000 и >= 1001. Однако такой вариант не подойдет для
        формул excel, которые я не могу поменять и поэтому явным образом в этом
        методе удаляем у полей, которых это касается знаки '='.

        Также подготавливаем словарь вида <ячейка_для_вставки>: <значение>,
        который будет использоваться в методе __input_cells() для вставки
        значений.

        Parameters
        ----------
        - cells_input : dict
            Словарь, с данными типа <Имя_поля>: <Адрес_ячейки_для_записи>.

        Returns
        -------
        - data_prepared : dict
            Отвалидированные и подготовленные для дальнейшей обработки данные.
        """

        # Подготавливаем данные для записи в Excel
        data_prepared = {}
        for name, cell in cells_input.items():
            if name in self.data.keys():
                if isinstance(self.data[name], str):
                    self.data[name] = self.data[name].replace(
                        sett.EQUALS_SYMBOL,
                        sett.EMPTY_STRING
                    ).strip()
                # Номер ячейки      = Значение переданных данных
                data_prepared[cell] = self.data[name]
        return data_prepared

    def check_data(self) -> bool:
        """
        Используя валидатор проверяет данные согласно определенным правилам,
        указанным в конфигурационном файле.

        Пробегаемся по ключам в переданных данных. Если такой ключ есть в
        правилах, то уже пробегаемся по самим правилам и по каждому правилу
        валидируем текущее значение по ключу из данных.

        Returns
        -------
        - _: bool
            Результат валидации данных.
        """

        for key, value in self.data.items():
            if key in self.rules:
                for rule_key, rule_value in self.rules[key].items():
                    if not Validator().validate(rule_key, rule_value, value):
                        check_err_mesg = self.__set_err_msg(
                            rule_key,
                            rule_value,
                            key,
                            value
                        )
                        return {
                            sett.CHECK_RESULT: False,
                            sett.ERROR_MESSAGE: check_err_mesg
                        }
        return {sett.CHECK_RESULT: True}

    def decimalize_and_rounding(
        self,
        excel_data: dict,
        roundings: dict[str, str] | None
    ) -> dict:
        """
        Переводит в Децимал и округляет значения по заданным параметрам или
        по умолчанию (до 2х цифр после запятой).

        Parameters
        ----------
        - excel_data: dict
            Словарь со значениями для перевода.

        - roundings: dict[str, str] | None
            Словарь с параметрами округления если оно отличается от
            стандартного.

        Returns
        -------
        - excel_data: dict
            Словарь с переведенными значениями.
        """

        # Перевод в Децимал и округление.
        for key, value in excel_data.items():
            if isinstance(value, str):
                match = re.search(sett.FLOAT_REGEX, value)
                if match:
                    number_str = match.group().replace(
                        sett.COMMA_SYMBOL,
                        sett.POINT_SYMBOL
                    )
                    value = number_str
            if (
                value and
                str(value).replace(
                    sett.POINT_SYMBOL,
                    sett.EMPTY_STRING,
                    sett.SET_TO_ONE).isdigit() and
                float(value) > sett.SET_TO_ZERO
            ):
                if roundings and (round_limit := roundings.get(key)):
                    excel_data[key] = Decimal(value).quantize(
                        Decimal(round_limit),
                        rounding=ROUND_HALF_UP
                    )
                else:
                    excel_data[key] = Decimal(value).quantize(
                        Decimal(sett.ROUNDING_LIMIT),
                        rounding=ROUND_HALF_UP
                    )

            if (
                not isinstance(
                    excel_data[key],
                    Decimal
                ) or excel_data[key] < sett.SET_TO_ZERO
            ):
                excel_data[key] = None

        return excel_data

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __set_err_msg(
        self,
        rule_key,
        rule_value,
        key,
        value
    ) -> str:
        """
        В зависимости от того, какой тип валидации не прошло значение,
        формирует сообщение об ошибке.

        Parameters
        ----------
        - rule_key: str
            Имя правила, которое было провалено (например max, min и т.д.).
        - rule_value: Any
            Значение правила, которое было не соблюдено.
        - key: str
            Имя параметра, значение которого провалило валидацию.
        - value: Any
            Значение параметра, провалившего валидацию.

        Returns
        -------
        - _: str
            Сообщение об ошибке
        """

        key = Translator.translate_string(key)

        match rule_key:

            case sett.VALIDATION_MIN:
                return sett.MIN_FAILED_MSG.format(key, rule_value, value)

            case sett.VALIDATION_MAX:
                return sett.MAX_FAILED_MSG.format(key, rule_value, value)

            case sett.VALIDATION_NUMERIC:
                return sett.NUM_FAILED_MSG.format(key, value)

            case sett.VALIDATION_NATURAL:
                return sett.NAT_FAILED_MSG.format(key, value)

            case sett.VALIDATION_MULTIPLE:
                return sett.MULT_FAILED_MSG.format(key, rule_value, value)

            case sett.VALIDATION_EXISTS:
                return sett.EXISTS_FAILED_MSG.format(key)

            case sett.VALIDATION_NOT_EQUAL:
                return sett.NOT_EQUAL_FAILED_MSG.format(key, rule_value, value)

            case _:
                return sett.EMPTY_STRING
