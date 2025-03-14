class Finder:
    def __init__(self):
        pass

    def find_layout_by_name(self, widgets, layout_name):
        """Рекурсивно ищет layout с нужным именем внутри вложенных структур."""
        for widget in widgets:
            if "layout" in widget:
                layout_config = widget["layout"]
                if layout_config.get("name") == layout_name:
                    return layout_config  # Нашли нужный layout
                # Рекурсивный поиск во вложенных виджетах
                found = self.find_layout_by_name(
                    layout_config.get("widgets", []),
                    layout_name
                )
                if found:
                    return found
        return None  # Если ничего не нашли
