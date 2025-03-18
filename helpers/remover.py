class Remover:
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

    def clean_up_fields(self, input_fields, chosen_fields):
        """Удаляет мёртвые ссылки из словарей input_fields и chosen_fields"""

        chosen_fields_to_delete = [
            name for name, field in chosen_fields.items()
            if self._is_invalid_widget(field, "currentText")
        ]

        input_fields_to_delete = [
            name for name, field in input_fields.items()
            if self._is_invalid_widget(field, "text")
        ]

        for name in chosen_fields_to_delete:
            chosen_fields.pop(name, None)

        for name in input_fields_to_delete:
            input_fields.pop(name, None)

    def _is_invalid_widget(self, widget, method):
        """Проверяет, выбросит ли метод RuntimeError (значит, виджет мёртв)"""
        try:
            getattr(widget, method)()  # Вызываем метод динамически
            return False
        except RuntimeError:
            return True
