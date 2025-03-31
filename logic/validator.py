from typing import Any

from logic.logger import logger as log
from helpers.helper import Helper
from settings import settings as sett


class Validator:
    """Класс для валидации данных.

    Methods
    -------
        validate()
            Валидирует данные по 1
    """

    @staticmethod
    def validate(rule_key: str, rule_value: Any, value: Any) -> bool:
        """
        Метод валидации данных. Вызывается отдельно для каждого параметра.

        Parameters
        ----------
            rule_key : str
                Ключ словаря правил для конкретного элемента шкафа. По ключу
                определяется как конкретно валиддировать параметр.
            rule_value : Any
                Значение, с которым сравнивается и на основании которого
                валадируется значение параметра.
            value : Any
                Значение, которое будет валидироваться.

        Return
        ------
            result: bool
                Результат валидации.
        """
        match rule_key:
            case sett.VALIDATION_MIN:
                log.info(f"Should be more than {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{value} is not numeric")
                    return False
                if value < rule_value:
                    log.error(
                        f"{value} is less than min possible ({rule_value})"
                    )
                    return False
            case sett.VALIDATION_MAX:
                log.info(f"'{rule_key}' should be less than {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{value} is not numeric")
                    return False
                if value > rule_value:
                    log.error(
                        f"{value} is greater than max possible ({rule_value})"
                    )
                    return False
            case sett.VALIDATION_NUMERIC:
                log.info(sett.SHOULD_BE_NUMERIC)
                if not str(value).isnumeric():
                    log.error(f"{value} is not numeric")
                    return False
            case sett.VALIDATION_NATURAL:
                log.info(sett.SHOULD_BE_NATURAL)
                if not str(value).isnumeric() or int(value) < 0:
                    log.error(f"{value} is not natural")
                    return False
            case sett.VALIDATION_MULTIPLE:
                log.info(f"Should be multiple of {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{value} is not numeric")
                    return False
                if value % rule_value != 0:
                    log.error(f"{value} is not multiple of {rule_value}")
                    return False
            case sett.VALIDATION_EXISTS:
                log.info(sett.SHOULD_BE_PRESENTED)
                if not value:
                    log.error(sett.EMPTY_REQUIRED_FIELDS)
                    return False

        log.info(sett.VALIDATION_IS_OK)
        return True

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

        for method in config[sett.CUSTOM_VALIDATIONS]:
            match method:
                case sett.SECTION_CHECK:
                    if not self.__check_section(data, config):
                        return {
                            sett.IS_CORRECT: False,
                            sett.ERROR_MESSAGE: sett.BASE_CHECK_FAILED
                        }
                case sett.DIAGONALS_CHECK:
                    if not self.__diagonals_check(data):
                        return {
                            sett.IS_CORRECT: False,
                            sett.ERROR_MESSAGE: sett.DIAGONALS_CHECK_FAILED
                        }
        return {
            sett.IS_CORRECT: True,
            sett.ERROR_MESSAGE: None
        }

    def __check_section(
        self,
        data: dict,
        config: dict
    ) -> bool:
        """
        Проверяет, если шкаф состоит из нескольких секций, то как минимум
        эти секции имеют одинаковую базу (но могут иметь разные толщины).

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
                    data[f"section_{i}"],
                    config[sett.CONVERTATION][f"section_{i}"]
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
        for i in range(sett.SET_TO_ONE, int(data[sett.PIECES])+1):
            expression = f"n_diagonals_{i} == n_traverse_{i} - 1"
            modified_expr = expression

            variables = {
                token for token
                in expression.replace('(', ' ').replace(')', ' ').split()
                if token.isidentifier()
            }
            for var in variables:
                total = sum(
                    int(value)
                    for key, value in data.items()
                    if key.startswith(var)
                    and isinstance(value, (int, float, str))
                    and str(value).replace(",", ".").replace(
                        ".", "", 1
                    ).isdigit()
                )

                modified_expr = modified_expr.replace(var, str(total))
            try:
                if not eval(modified_expr):
                    False
            except Exception:
                return False
        return True
