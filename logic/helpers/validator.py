import re

from typing import Any

from logic.helpers.helper import Helper
from logic.logger import LogManager as lm
from settings import settings as sett


class Validator:
    """
    Класс для валидации данных.

    Methods
    -------
    - custom_validation(config, data)
        Валидирует данные по кастомным правилам из конфига.

    - validate(rule_key, rule_value, value)
        Валидирует данные по 1 по стандартным правилам из конфига.

    - validate_email(email)
        Валидирует email адрес по регулярному выражению.

    - check_password_strength(password)
        Проверяет сложность пароля по стандартным критериям.

    Private Methods
    ---------------
    - __check_section(data, config)
        Проверяет, если шкаф состоит из нескольких секций, то как минимум
        эти секции имеют одинаковую базу (но могут иметь разные толщины).

    - __diagonals_check(data)
        Проверяет, что количество диагоналей на 1 меньше, чем траверс.
        Проверка осуществляется для каждой существующей секции независимо.
    """

    def custom_validation(
        self,
        config: list,
        data: dict
    ) -> bool:
        """
        По очереди вызывает тот или иной метод валидации из имеющихся
        приватных. Методы берутся из конфига.

        Parameters
        ----------
        - config : dict
                Конфиг расчетов, в котором указаны методы валидации.
        - data : dict[str, Any]
                Данные для проверки.

        Returns
        -------
        - _: dict
            Результат проверки. И сообщение об ошибке, если проверка не
            пройдена.
        """

        lm.log_method_call()
        for method in config[sett.CUSTOM_VALIDATIONS]:
            match method:
                case sett.SECTION_CHECK:
                    lm.log_info(sett.VALIDATE_SECTION)
                    if not self.__check_section(data, config):
                        lm.log_error(sett.SECTIONS_ARE_NOT_VALID)
                        return {
                            sett.IS_CORRECT: False,
                            sett.ERROR_MESSAGE: sett.BASE_CHECK_FAILED
                        }
                    lm.log_info(sett.SECTIONS_ARE_VALID)

                case sett.DIAGONALS_CHECK:
                    lm.log_info(sett.VALIDATE_DIAGONALS)
                    if not self.__diagonals_check(data):
                        lm.log_error(sett.DIAGONALS_ARE_NOT_VALID)
                        return {
                            sett.IS_CORRECT: False,
                            sett.ERROR_MESSAGE: sett.DIAGONALS_CHECK_FAILED
                        }
                    lm.log_info(sett.DIAGONALS_ARE_VALID)
        return {
            sett.IS_CORRECT: True,
            sett.ERROR_MESSAGE: None
        }

    @staticmethod
    def validate(rule_key: str, rule_value: Any, value: Any) -> bool:
        """
        Метод валидации данных. Вызывается отдельно для каждого параметра.

        Parameters
        ----------
        - rule_key : str
            Ключ словаря правил для конкретного элемента шкафа. По ключу
            определяется как конкретно валиддировать параметр.
        - rule_value : Any
            Значение, с которым сравнивается и на основании которого
            валадируется значение параметра.
        - value : Any
            Значение, которое будет валидироваться.

        Return
        ------
        - result: bool
            Результат валидации.
        """

        match rule_key:

            case sett.VALIDATION_MIN:
                lm.log_info(sett.SHOULD_BE_MORE_THAN, rule_key, rule_value)
                try:
                    value = int(value)
                except ValueError:
                    return False
                if value < rule_value:
                    lm.log_error(sett.IS_LESS_THAN, value, rule_value)
                    return False

            case sett.VALIDATION_MAX:
                lm.log_info(sett.SHOULD_BE_LESS_THAN, rule_key, rule_value)
                try:
                    value = int(value)
                except ValueError:
                    return False
                if value > rule_value:
                    lm.log_error(sett.IS_GREATER_THAN, value, rule_value)
                    return False

            case sett.VALIDATION_NUMERIC:
                lm.log_info(sett.SHOULD_BE_NUMERIC, rule_key)
                if not str(value).isnumeric():
                    lm.log_error(sett.IS_NOT_NUMERIC, value)
                    return False

            case sett.VALIDATION_NATURAL:
                lm.log_info(sett.SHOULD_BE_NATURAL, rule_key)
                if not str(value).isnumeric() or int(value) < 0:
                    lm.log_error(sett.IS_NOT_NATURAL, value)
                    return False

            case sett.VALIDATION_MULTIPLE:
                lm.log_info(sett.SHOULD_BE_MULTIPLE, rule_key, rule_value)
                try:
                    value = int(value)
                except ValueError:
                    return False
                if value % rule_value != 0:
                    lm.log_error(sett.IS_NOT_MULTIPLE, value, rule_value)
                    return False

            case sett.VALIDATION_EXISTS:
                lm.log_info(sett.SHOULD_BE_PRESENTED, rule_key)
                if not value:
                    lm.log_error(sett.IS_NOT_PRESENTED, rule_key, value)
                    return False

            case sett.VALIDATION_NOT_EQUAL:
                lm.log_info(sett.SHOULD_NOT_BE_EQUAL, rule_key, rule_value)
                if int(value) == int(rule_value):
                    lm.log_error(sett.IS_EQUAL, value, rule_value)
                    return False

        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Метод валидации email адреса. Проверяет, что email адрес имеет
        корректный формат.

        Parameters
        ----------
            email : str
                Email адрес для проверки.

        Return
        ------
            result: bool
                Результат валидации.
        """

        if re.match(sett.EMAIL_REGEX, email):
            lm.log_info(sett.EMAIL_IS_VALID)
            return True

        lm.log_error(sett.EMAIL_IS_NOT_VALID)
        return False

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Метод валидации телефонного номера. Проверяет, что номер имеет
        корректный формат.
        """

        if re.match(sett.PHONE_REGEX, phone):
            lm.log_info(sett.PHONE_IS_VALID)
            return True

        lm.log_error(sett.PHONE_IS_NOT_VALID.format(phone))
        return False

    @staticmethod
    def check_password_strength(password: str) -> bool:
        """
        Проверяет сложность пароля. Пароль должен содержать:
        - минимум 8 символов,
        - минимум 1 цифру,
        - минимум 1 заглавную букву,
        - минимум 1 строчную букву,
        - минимум 1 специальный символ.

        Parameters
        ----------
        - password: str
            Пароль для проверки.

        Returns
        -------
        - _: bool
            True, если пароль соответствует критериям сложности, иначе False.
        """

        lm.log_info(sett.CHECK_PASSWORD_STRENGTH)
        if len(password) < sett.MIN_PASS_LENGTH:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char in sett.SPECIAL_CHARS for char in password):
            return False
        return True

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __check_section(
        self,
        data: dict,
        config: dict
    ) -> bool:
        """
        Проверяет, если шкаф состоит из нескольких секций, то как минимум
        эти секции имеют одинаковую базу (но могут иметь разные толщины).
        Принцип работы проверки:
        1. Пробегаемся по каждорй из секций шкафа (Если секия одна, то
           сразу возвращаем True).
        2. Выписываем все секции в отдельный список, отсекая толщины и оставляя
           только типоразмер базы.
        3. Конвертируем список в множество, чтобы исключить повторения.
        4. Если длина множества равна 1, т.е. если все типоразмеры
           соответствуют первому, возвращаем True, иначе False.

        Parameters
        ----------
        - data : dict[str, Any]
            Данные для проверки.
        - config : dict[str, Any]
            Конфиг расчетов, в котором указаны методы валидации.

        Return
        ------
        - bool
            Результат проверки базы на одинаковость.
        """

        if int(data[sett.PIECES]) == sett.SET_TO_ONE:
            return True

        sections: list[str] = []
        for i in range(sett.SET_TO_ONE, int(data[sett.PIECES])+1):
            sections.append(
                Helper.backward_convertation(
                    data[sett.SECTION_I.format(i)],
                    config[sett.CONVERTATION][sett.SECTION_I.format(i)],
                )
            )

        sections = [
            section.split(sett.SLASH)[sett.SET_TO_ZERO]
            for section in sections
        ]

        return len(set(sections)) == sett.SET_TO_ONE

    def __diagonals_check(
        self,
        data: dict[str, Any],
    ):
        """
        Проверяет, что количество диагоналей секции на 1 меньше, чем
        количество траверс. Проверка осуществляется для каждой существующей
        секции независимо от других.

        Parameters
        ----------
        - data : dict[str, Any]
            Данные для проверки.

        Returns
        -------
        - _: bool
            Результат проверки количества диагоналей и количество траверс.
        """

        for i in range(sett.SET_TO_ONE, int(data[sett.PIECES])+1):
            expression = sett.DIAGONALS_TRAVERSE.format(i)
            modified_expr = expression

            variables = {
                token for token
                in expression.replace(
                    sett.LEFT_BRACKET_SYMBOL,
                    sett.SPACE_SYMBOL
                ).replace(
                    sett.RIGHT_BRACKET_SYMBOL,
                    sett.SPACE_SYMBOL
                ).split()
                if token.isidentifier()
            }
            for var in variables:
                total = sum(
                    int(value)
                    for key, value in data.items()
                    if key.startswith(var)
                    and isinstance(value, (int, float, str))
                    and str(value).replace(
                        sett.COMMA_SYMBOL,
                        sett.POINT_SYMBOL
                    ).replace(
                        sett.POINT_SYMBOL, sett.EMPTY_STRING, 1
                    ).isdigit()
                )

                modified_expr = modified_expr.replace(var, str(total))
            try:
                if not eval(modified_expr):
                    return False
            except Exception:
                return False
        return True
