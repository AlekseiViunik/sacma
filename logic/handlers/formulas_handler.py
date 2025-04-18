import re

from decimal import Decimal, ROUND_HALF_UP

from logic.logger import LogManager as lm
from settings import settings as sett


class FormulasHandler:
    """
    Класс-обработчик формул.

    Methods
    -------
    - apply_formula(data, formula, formula_name)
        Выполняет математическое выражение по заданной в виде строки формуле и
        и возвращает результат вычисления формулы.

    - check_condition(data, condition)
        Применяет условие к данным и возвращает True, если условие выполнено.
    """

    def apply_formula(
        self,
        data: dict,
        formula: str,
        formula_name: str = sett.PRICE
    ) -> Decimal:
        """
        Выполняет математическое выражение по заданной в виде строки формуле,
        заменяя переменные из словаря `data`. Формула может содержать числа,
        операторы +, -, *, /, скобки и числа.

        Parameters
        ----------
        - data: dict
            Данные, которые, возможно, нужно будет подставить в формулу.

        - formula: str
            Формула в виде строки.

        - formula_name: str
            Default = 'price'\n
            Имя формулы (ключ, по которому она хранилась в словаре формул
            в конфиге).

        Returns
        -------
        - result: Decimal
            Результат вычисления формулы.
        """

        # Проверяем, что в data все значения — Decimal
        if not all(isinstance(value, Decimal) for value in data.values()):
            lm.log_error(sett.NOT_DECIMAL_ERROR)
            raise ValueError(sett.NOT_DECIMAL_ERROR)

        # Извлекаем все переменные из формулы
        formula_vars = set(re.findall(sett.VARIABLE_REGEX, formula))

        # Проверяем, есть ли пропущенные переменные
        missing_vars = formula_vars - set(data.keys())

        if missing_vars:
            return data[formula_name]

        # Разбираем выражение, заменяя переменные их значениями
        def replace_var(match):
            var = match.group(0)  # Получаем название переменной
            if var not in data:
                lm.log_error(sett.VAR_IS_MISSING, var)
                raise KeyError(sett.VAR_IS_MISSING.format(var))
            return str(data[var])  # Подставляем значение из словаря

        # Регулярное выражение для поиска переменных
        # (любых слов без пробелов и операторов)
        expression = re.sub(sett.VARIABLE_REGEX, replace_var, formula)

        # Проверяем, что в выражении остались только допустимые символы
        # (цифры, скобки, операторы)
        if not re.match(sett.NUMBERS_N_OPERATORS_REGEX, expression):
            lm.log_error(sett.UNACCEPTABLE_OPERATORS)
            raise ValueError(sett.UNACCEPTABLE_OPERATORS)

        # Выполняем вычисление
        result = Decimal(eval(expression)).quantize(
                    Decimal(sett.ROUNDING_LIMIT),
                    rounding=ROUND_HALF_UP
                )
        return result

    def check_condition(
        self,
        data: dict,
        condition: str
    ) -> bool:
        """
        Применяет условие к данным и возвращает True, если условие выполнено.
        само условие должно быть в виде строки, например:
        "price > 100 and quantity < 50".

        Parameters
        ----------
        - data: dict
            Все собранные данные, в которых содержаться переменные для
            подстановки в условие.

        - condition: str
            Условие в виде строки, например: "price > 100 and quantity < 50".

        Returns
        -------
        - _: bool
            Результат выполнения строкового условия с подставленными данными.
        """

        for key in data:
            if key in condition:
                value = (
                    repr(data[key]) if isinstance(data[key], str)
                    else str(data[key])
                )
                condition = condition.replace(key, value)
        try:
            return eval(condition)
        except Exception:
            return False
