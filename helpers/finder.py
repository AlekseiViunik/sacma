from typing import List


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
            if "layout" in widget:

                # Берем его конфиг
                layout_config = widget["layout"]

                # И смотрим, если это контейнер с искомым именем, то
                if layout_config.get("name") == layout_name:

                    # Возвращаем его.
                    return layout_config

                # Иначе вызываем повторно текущий метод, куда передаем конфиг
                # контейнера, который сейчас среди виджетов и его имя.
                found = self.find_layout_by_name(
                    layout_config.get("widgets", []),
                    layout_name
                )
                if found:
                    return found
        return None  # Если ничего не нашли
