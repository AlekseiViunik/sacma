class LayoutRemover:
    def __init__(self):
        pass

    def delete_layout(self, parent_widget, layout_to_delete=None):
        if not layout_to_delete:
            return  # Если layout отсутствует, ничего не делаем

        parent_layout = parent_widget.layout()
        if not parent_layout:
            return  # Если у родителя нет layout, тоже ничего не делаем

        # Очищаем layout от виджетов и вложенных layout'ов
        self.__clear_layout(layout_to_delete)
        parent_layout.removeItem(layout_to_delete)
        layout_to_delete.deleteLater()  # Удаляем объект

    def __clear_layout(self, layout_to_clear):
        while layout_to_clear.count():
            item = layout_to_clear.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.__clear_layout(item.layout())
                item.layout().deleteLater()
