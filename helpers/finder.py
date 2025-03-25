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
