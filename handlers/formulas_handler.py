import re
from decimal import Decimal, ROUND_HALF_UP


class FormulasHandler:

    def apply_formula(self, data, formula):
        """
        Выполняет математическое выражение, заменяя переменные из словаря
        `data`.
        """

        # Проверяем, что в data все значения — Decimal
        if not all(isinstance(value, Decimal) for value in data.values()):
            raise ValueError("Все значения в `data` должны быть типа Decimal")

        # Разбираем выражение, заменяя переменные их значениями
        def replace_var(match):
            var = match.group(0)  # Получаем название переменной
            if var not in data:
                raise KeyError(f"Переменная '{var}' отсутствует в data")
            return str(data[var])  # Подставляем значение из словаря

        # Регулярное выражение для поиска переменных
        # (любых слов без пробелов и операторов)
        expression = re.sub(r"[a-zA-Z_][a-zA-Z0-9_]*", replace_var, formula)

        # Проверяем, что в выражении остались только допустимые символы
        # (цифры, скобки, операторы)
        if not re.match(r"^[0-9.\s()+\-*/]+$", expression):
            raise ValueError("Выражение содержит недопустимые символы")

        # Выполняем вычисление
        result = Decimal(eval(expression)).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )
        return result
