from typing import Any
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout
)

from settings import settings as set


class Remover:
    """
    Класс-помощник. Удаляет то, что надо.

    Methods
    -------
    - delete_layout(parent_widget, layout_to_delete)
        Удаляет контейнер.

    - clean_up_fields(input_fields, chosen_fields)
        Удаляет мертвые ссылки из словарей с введенными юзером данными.

    Private methods
    ---------------
    - __is_invalid_widget(widget, method)
        Проверяет, живой ли виджет или это мертвая ссылка, которую нужно
        удалить.

    - __clear_layout(layout_to_clear)
        Очищает контейнер от виджетов перед его удалением.
    """

    def delete_layout(
        self,
        parent_widget: QGridLayout | QHBoxLayout | QVBoxLayout,
        layout_to_delete: QGridLayout | QHBoxLayout | QVBoxLayout | None = None
    ) -> None:
        """
        Удаляет контейнер, чтобы на его место вставить такой же, только
        обновленный.

        Parameters
        ----------
        - parent_widget: QGridLayout | QHBoxLayout | QVBoxLayout
            Родительский виджет, на котором расположен текущий контейнер,
            который надо удалить.

        - layout_to_delete: QGridLayout | QHBoxLayout | QVBoxLayout | None
            Виджет, который надо удалить.
        """

        # Если layout отсутствует, ничего не делаем.
        if not layout_to_delete:
            return

        # Если у родителя нет layout, тоже ничего не делаем.
        parent_layout = parent_widget.layout()
        if not parent_layout:
            return

        # Очищаем layout от виджетов и вложенных layout'ов.
        self.clear_layout(layout_to_delete)

        parent_layout.removeItem(layout_to_delete)
        layout_to_delete.deleteLater()  # Удаляем объект

    def clean_up_fields(
        self,
        input_fields: dict,
        chosen_fields: dict
    ) -> None:
        """
        Удаляет мёртвые ссылки из словарей input_fields и chosen_fields.

        Parameters
        ----------
        - input_fields: dict
            Введенные пользователем данные.
        - chosen_fields: dict
            Выбранные пользователем данные.
        """

        # Формируем списки полей для удаления.
        chosen_fields_to_delete = [
            name for name, field in chosen_fields.items()
            if self.__is_invalid_widget(field, set.CURRENT_TEXT_METHOD)
        ]
        input_fields_to_delete = [
            name for name, field in input_fields.items()
            if self.__is_invalid_widget(field, set.TEXT_METHOD)
        ]

        # Пробегаемся по этим спискам и удаляем поля из словарей.
        for name in chosen_fields_to_delete:
            chosen_fields.pop(name, None)

        for name in input_fields_to_delete:
            input_fields.pop(name, None)

    def __is_invalid_widget(
        self,
        widget: Any,
        method: str
    ) -> bool:
        """
        Проверяет, выбросит ли метод RuntimeError (значит, виджет мёртв).

        Parameters
        ----------
        - widget: Any
            Любой из виджетов или мертвая ссылка на виджет.

        - method: str
            Имя метода, который должен быть у этого виджета, который
            представлен в виде строки. Если у виджета этого метода нет, то и
            виджет мертв.

        Returns
        -------
        - _: bool
            Информация о том, мертв ли виджет. Если True, значит мертв.
        """

        try:
            getattr(widget, method)()  # Вызываем метод динамически
            return False
        except RuntimeError:
            return True

    def clear_layout(
        self,
        layout_to_clear: QGridLayout | QHBoxLayout | QVBoxLayout
    ) -> None:
        """
        Рекурсивный метод очистки и удаления контейнеров.
        Поскольку непустой контейнер нельзя удалить, то сначала очищаем его.
        Принцип:
        - Если в контейнере расположен еще один контейнер, то метод вызывает
        сам себя для того контейнера.
        - Если в контейнере нет виджетов, удаляет контейнер.
        - Если в контейнере есть виджеты, удаляет виджет.

        Parameters
        ----------
        - layout_to_clear: QGridLayout | QHBoxLayout | QVBoxLayout
            Контейнер, который надо удалить.
        """

        # Пока в контейнере что-то есть:
        while layout_to_clear.count():

            # берем первый элемент контейнера.
            item = layout_to_clear.takeAt(set.SET_TO_ZERO)

            # Если элемент - виджет, удаляем его.
            if item.widget():
                item.widget().deleteLater()

            # Если элемент - контейнер, сначала очищаем, вызывая этот же метод,
            # а потом удаляем его.
            elif item.layout():
                self.clear_layout(item.layout())
                item.layout().deleteLater()
