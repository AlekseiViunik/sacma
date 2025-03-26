from typing import List

from settings import settings as set


class Finder:
    """
    Хелпер поисковик. Что-то ищет.

    Methods
    -------
    - find_layout_by_name(widgets, layout_name)
        Ищет конфиг контейнера по имени.
    """

    def find_layout_by_name(
        self,
        widgets: List[dict],
        layout_name: str
    ) -> dict:
        """
        Рекурсивно ищет layout (его конфиг) с нужным именем внутри вложенных
        структур.

        Parameters
        ----------
        - widgets: List[dict]
            Список кофигов для виджетов текущего контейнера, среди которого
            могут быть также контейнеры.

        - layout: str
            Имя текущего контейнера.

        Returns
        -------
        - found: dict | None
            Найденный конфиг контейнера с его виджетами.
        """

        # Пробегаемся по виджетам текущего контейнера.
        for widget in widgets:

            # Если среди виджетов есть контейнер, то
            if set.LAYOUT in widget:

                # Берем его конфиг
                layout_config = widget[set.LAYOUT]

                # И смотрим, если это контейнер с искомым именем, то
                if layout_config.get(set.NAME) == layout_name:

                    # Возвращаем его.
                    return layout_config

                # Иначе вызываем повторно текущий метод, куда передаем конфиг
                # контейнера, который сейчас среди виджетов и его имя.
                found = self.find_layout_by_name(
                    layout_config.get(set.WIDGETS, []),
                    layout_name
                )
                if found:
                    return found
        return None  # Если ничего не нашли

    def find_all_widget_names_by_type(
        self,
        layout_config: dict,
        type: str = set.LABEL,
        widget_names: list = []
    ) -> list:
        """
        Ищет в словаре конфига все виджеты указанного типа и возвращает список
        их имен. Пока что используется только в тестах.

        Parameters
        ----------
        - layout_config: dict
            Конфиг, в котором будет происходить поиск.

        - type: str
            Тип, виджеты которого нужно искать.

        - widget_names: list
            Список имен словаря. Изначально пустой.

        Returns
        -------
        - widget_names: list
            Список имен найденных виджетов указанного типа.
        """

        widgets = layout_config.get(set.WIDGETS, [])

        for widget in widgets:
            if set.LAYOUT in widget:
                self.find_all_widget_names_by_type(
                    widget[set.LAYOUT],
                    type,
                    widget_names
                )
            elif widget.get(set.TYPE) == type:
                widget_names.append(widget[set.TEXT])
        return widget_names

    def find_and_count_all_widgets(
        self,
        layout_config: dict,
        counter: int = set.SET_TO_ZERO
    ) -> int:
        """
        Считает, сколько всего виджетов должно быть установлено по конфигу
        для окна. Пока что используется только в тестах. Работает только для
        статичных окон, которые не перерисовываются во время работы приложения.

        Parameters
        ----------
        - layout_config: dict
            Конфиг, в котором будет происходить поиск.

        - counter: int
            Счетчик, который каждый раз при нахождении виджета (не контейнера)
            увеличивается на +1

        Returns
        -------
        - counter: int
            Итоговоый счетчик после подсчета.
        """
        widgets = layout_config.get(set.WIDGETS, [])
        counter = set.SET_TO_ZERO
        for widget in widgets:
            if set.LAYOUT in widget:
                counter += self.find_and_count_all_widgets(
                    widget[set.LAYOUT],
                    counter
                )
            else:
                counter += set.STEP_UP
        return counter
