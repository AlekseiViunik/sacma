import re
from decimal import Decimal, ROUND_HALF_UP


class FormulasHandler:
    """
    Класс-обработчик формул.

    Methods
    -------
    - apply_formula(data, formula, formula_name)
        Выполняет математическое выражение по заданной в виде строки формуле и
        и возвращает результат вычисления формулы.
    """
    def apply_formula(
        self,
        data: dict,
        formula: str,
        formula_name: str = "price"
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
            Имя формулы (ключ, по которому она хранилась в словаре формул
            в конфиге).

        Returns
        -------
        - result: Decimal
            Результат вычисления формулы.
        """

        # Проверяем, что в data все значения — Decimal
        if not all(isinstance(value, Decimal) for value in data.values()):
            raise ValueError("Все значения в `data` должны быть типа Decimal")

        # Извлекаем все переменные из формулы
        formula_vars = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", formula))

        # Проверяем, есть ли пропущенные переменные
        missing_vars = formula_vars - set(data.keys())

        if missing_vars:
            return data[formula_name]

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
