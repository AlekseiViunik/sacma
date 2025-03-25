from typing import Any

from logic.logger import logger as log
from settings import settings as set


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
            case set.VALIDATION_MIN:
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
            case set.VALIDATION_MAX:
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
            case set.VALIDATION_NUMERIC:
                log.info(set.SHOULD_BE_NUMERIC)
                if not str(value).isnumeric():
                    log.error(f"{value} is not numeric")
                    return False
            case set.VALIDATION_NATURAL:
                log.info(set.SHOULD_BE_NATURAL)
                if not str(value).isnumeric() or int(value) < 0:
                    log.error(f"{value} is not natural")
                    return False
            case set.VALIDATION_MULTIPLE:
                log.info(f"Should be multiple of {rule_value}")
                try:
                    value = int(value)
                except ValueError:
                    log.error(f"{value} is not numeric")
                    return False
                if value % rule_value != 0:
                    log.error(f"{value} is not multiple of {rule_value}")
                    return False
        log.info(set.VALIDATION_IS_OK)
        return True
