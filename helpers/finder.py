from settings import settings as sett


class Finder:
    """
    Хелпер поисковик. Что-то ищет.

    Methods
    -------
    - find_layout_by_name(widgets, layout_name)
        Ищет конфиг контейнера по имени.

    - find_all_widget_names_by_type(layout_config, type, widget_names)
        Ищет все виджеты указанного типа и возвращает список их имен.

    - find_and_count_all_widgets(layout_config, counter)
        Считает, сколько всего виджетов должно быть установлено по конфигу
        для окна. Работает только для статичных окон, которые не
        перерисовываются во время работы приложения.

    - find_all_active_widgets(layout_config, activity_type, widgets_list)
        Ищет все виджеты, которые активны в данный момент. Возвращает список
        виджетов, которые активны в данный момент.
    """

    def find_layout_by_name(
        self,
        widgets: list[dict],
        layout_name: str
    ) -> dict | None:
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
            if sett.LAYOUT in widget:

                # Берем его конфиг
                layout_config = widget[sett.LAYOUT]

                # И смотрим, если это контейнер с искомым именем, то
                if layout_config.get(sett.NAME) == layout_name:

                    # Возвращаем его.
                    return layout_config

                # Иначе вызываем повторно текущий метод, куда передаем конфиг
                # контейнера, который сейчас среди виджетов и его имя.
                found = self.find_layout_by_name(
                    layout_config.get(sett.WIDGETS, []),
                    layout_name
                )
                if found:
                    return found
        return None  # Если ничего не нашли

    def find_all_widget_names_by_type(
        self,
        layout_config: dict,
        type: str = sett.LABEL,
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

        widgets = layout_config.get(sett.WIDGETS, [])

        for widget in widgets:
            if sett.LAYOUT in widget:
                self.find_all_widget_names_by_type(
                    widget[sett.LAYOUT],
                    type,
                    widget_names
                )
            elif widget.get(sett.TYPE) == type:
                widget_names.append(widget[sett.TEXT])
        return widget_names

    def find_and_count_all_widgets(
        self,
        layout_config: dict,
        counter: int = sett.SET_TO_ZERO
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

        widgets = layout_config.get(sett.WIDGETS, [])
        counter = sett.SET_TO_ZERO
        for widget in widgets:
            if sett.LAYOUT in widget:
                counter += self.find_and_count_all_widgets(
                    widget[sett.LAYOUT],
                    counter
                )
            else:
                counter += sett.STEP_UP
        return counter

    def find_all_active_widgets(
        self,
        layout_config: dict,
        activity_type: str,
        widgets_list: list | None = None
    ) -> list:
        """
        Рекурсивно ищет все виджеты, которые активны в данный момент.
        Возвращает список этих виджетов. Создан для тестов.

        Parameters
        ----------
        - layout_config: dict
            Конфиг, в котором будет происходить поиск.

        - activity_type: str
            Тип активности виджета, который нужно искать.

        - widgets_list: list | None
            Формируемый список найденных виджетов для текущего уровня рекурсии.
            Изначально пустой.

        Returns
        -------
        - widgets_list: list
            Список виджетов, которые активны в данный момент.
        """

        if widgets_list is None:
            widgets_list = []

        widgets = layout_config.get(sett.WIDGETS, [])
        for widget in widgets:
            if sett.LAYOUT in widget:
                self.find_all_active_widgets(
                    widget[sett.LAYOUT],
                    activity_type,
                    widgets_list
                )
            else:
                availability = widget.get(sett.ACTIVE_WHEN)
                if availability and activity_type not in availability:
                    continue
                widgets_list.append(widget)

        return widgets_list
