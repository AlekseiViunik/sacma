from PyQt6.QtWidgets import (QLineEdit, QComboBox)
from typing import Dict

from helpers.remover import Remover


class InputDataHandler:
    """
    Обработчик данных, введенных/выбранных пользователем.

    Attributes
    ----------
    - remover: Remover
        Один из помощников, который удаляет ненужные данные.

    Methods
    -------
    - collect_all_inputs(input_fields, choice_fields)
        Объединяет словари с введенными и выбранными данными.

    - check_mandatory(inputs, choice_fields)
        Проверяет, какие поля из обязательных не заполнены и возвращает
        список этих полей.
    """

    def __init__(self) -> None:
        self.remover: Remover = Remover()

    def collect_all_inputs(
        self,
        input_fields: Dict[str, QLineEdit],
        choice_fields: Dict[str, QComboBox]
    ) -> dict:
        """
        Объединяет два словаря в один. На входе словарь с введеными значениями
        и словарь с выбранными значениями. В значениях записаны обхекты
        виджетов. На выходе общий словарь со значениями юзера. Сами значения
        преобразуются в текст.

        Parameters
        ----------
        - input_fields: dict
            Введенные юзером значения.

        - choice_fields: dict
            Выбранные юзером значения.

        Returns
        -------
        - all_inputs: dict
            Обобщенный словарь входных данных.
        """

        # Когда изменяющий виджет меняет расклад виджетов на окне, некоторые
        # виджеты должны исчезнуть. Они удаляются из окна, но не из словаря
        # введенных значений. В итоге они лежат там как мертвые ссылки, от
        # которых нужно избавиться, чтобы не выбрасывалась ошибка.
        self.remover.clean_up_fields(
            input_fields,
            choice_fields
        )
        all_inputs = {}

        # Добавляем в обобщенный словарь выбранные юзером данные в виде текста.
        for name, field in choice_fields.items():
            all_inputs[name] = field.currentText()

        # Добавляем в обобщенный словарь введенные юзером данные в виде текста.
        for name, field in input_fields.items():
            all_inputs[name] = field.text()
        return all_inputs

    def check_mandatory(
        self,
        inputs: dict,
        mandatories: list
    ) -> list:
        """
        Проверяет заполнение обязательных полей.
        Использует вычитание множеств. Из множества обязательных полей
        вычитается множетсво заполненных полей. Возвращается список по
        результатам вычитания.

        Parameters
        ----------
        - inputs: dict
            Словарь заполненных юзером полей.

        - mandatories: list
            Список обязательных полей для заполнения, сформированный из
            конфига.

        Returns
        -------
        - _: list
            список обязательных, но не заполненных полей.
        """

        # Составляем множество ключей из словаря введенных юзером данных
        # Если для этого ключа есть значение (если юзер его ввел/выбрал).
        filled_inputs = {k for k, v in inputs.items() if v}

        # Возвращаем результат в виде разности множеств преобразованной в
        # список.
        return list(set(mandatories) - filled_inputs)
