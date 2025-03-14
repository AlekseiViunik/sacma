from typing import Any
from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget
)

from helpers.remover import Remover
from helpers.finder import Finder


class Creator:

    def __init__(
        self,
        config: dict,
        parent_window: Any
    ) -> None:
        self.config = config
        self.parent_window = parent_window  # Нужно для закрытия окна
        self.input_fields = {}
        self.chosen_fields = {}
        self.default_values = {}
        self.current_changing_value = None
        self.dependencies = {}
        self.remover = Remover()
        self.finder = Finder()

    def create_widget_layout(
        self,
        parent_window: QHBoxLayout | QVBoxLayout | QGridLayout | QWidget,
        layout_config: dict | None
    ) -> None:
        """
        Создает контейнер для размещения виджетов.
        """

        # Create layout and place widgets on it
        if layout_config:
            if layout_config.get('depends_on'):
                self.current_changing_value = self.default_values[
                    layout_config['depends_on']
                ]
                if (
                    layout_config['depends_on'] in self.dependencies and
                    self.dependencies[
                        layout_config['depends_on']
                    ].get(layout_config['name'])
                ):
                    self.remover.delete_layout(
                        parent_window,
                        self.dependencies[
                            layout_config['depends_on']
                        ][layout_config['name']]
                    )
            layout = self.__create_layout(layout_config)
            self.__add_widgets(
                layout,
                layout_config['type'],
                layout_config['widgets'],
                layout_config.get('columns')
            )

        # add/set Layout to the parent window
        if (
            isinstance(parent_window, QHBoxLayout) or
            isinstance(parent_window, QVBoxLayout) or
            isinstance(parent_window, QGridLayout)
        ):
            parent_window.addLayout(layout)
        else:
            parent_window.setLayout(layout)

    def __add_widgets(
        self,
        layout: QHBoxLayout | QVBoxLayout | QGridLayout,
        layout_type: str,
        widgets_configs: list,
        columns: int | None = None
    ) -> None:
        match layout_type:
            case "grid":
                current_row = 0
                current_column = 0
                for widget_config in widgets_configs:
                    if not self.__check_if_widget_is_active(widget_config):
                        continue
                    current_row, current_column = self.__get_widget_pos(
                        current_row,
                        current_column,
                        columns,
                        widget_config.get('column')
                    )
                    self.__create_widget(
                        widget_config,
                        layout,
                        current_row,
                        current_column
                    )

                    current_column = current_column + 1
            case "vertical" | "horizontal":
                for widget_config in widgets_configs:
                    if not self.__check_if_widget_is_active(widget_config):
                        continue
                    self.__create_widget(widget_config, layout)

    def __create_widget(
        self,
        config: dict,
        layout: QHBoxLayout | QVBoxLayout | QGridLayout | None = None,
        row: int | None = None,
        column: int | None = None
    ) -> None:
        if config.get('layout'):
            self.create_widget_layout(
                layout,
                config['layout']
            )
        else:
            match config.get('type'):
                case "label":
                    widget = self.__create_label(config)
                case "input":
                    widget = self.__create_input(config)
                case "button":
                    widget = self.__create_button(config)
                case "dropdown":
                    widget = self.__create_dropdown(config)
                case _:
                    widget = None
            if widget:
                if row is not None and column is not None:
                    layout.addWidget(widget, row, column)
                else:
                    layout.addWidget(widget)

    def __create_layout(
        self,
        layout_config: dict
    ) -> QHBoxLayout | QVBoxLayout | QGridLayout | None:

        match layout_config["type"]:
            case "grid":
                layout = QGridLayout()
            case "vertical":
                layout = QVBoxLayout()
            case "horizontal":
                layout = QHBoxLayout()
        # Простая проверка if layout тут не подойдет. Почему - хз, видимо,
        # потому что сам объект пустой пока
        if isinstance(layout, (QGridLayout, QVBoxLayout, QHBoxLayout)):
            if 'depends_on' in layout_config:
                self.dependencies.setdefault(
                    layout_config['depends_on'], {}
                )[layout_config['name']] = layout

            return layout
        return None

    def __create_label(self, config: dict) -> QLabel:
        return QLabel(config['text'])

    def __create_input(self, config: dict) -> QLineEdit:
        input_field = QLineEdit()
        for param, value in config.items():
            match param:
                case "width":
                    input_field.setFixedWidth(int(value))
                case "height":
                    input_field.setFixedHeight(int(value))
                case "default_value":
                    input_field.setPlaceholderText(value)
        self.input_fields[config['name']] = input_field
        return input_field

    def __create_button(self, config: dict) -> QPushButton:
        button = QPushButton(config['text'])
        for param, value in config.items():
            match param:
                case "width":
                    button.setFixedWidth(int(value))
                case "height":
                    button.setFixedHeight(int(value))
                case "callback":
                    self.parent_window.connect_callback(
                        button,
                        value,
                        config.get("params", {})
                    )
        if "callback" not in config:
            button.setEnabled(False)
        return button

    def __create_dropdown(self, config: dict):
        dropdown = QComboBox()
        self.default_values[config['name']] = config['default_value']
        for param, value in config.items():
            match param:
                case "options":
                    if value.get('always'):
                        dropdown.addItems(value['always'])
                    else:
                        dropdown.addItems(value[self.current_changing_value])
                case "width":
                    dropdown.setFixedWidth(int(value))
                case "height":
                    dropdown.setFixedHeight(int(value))
                case "default_value":
                    dropdown.setCurrentText(str(value))
        self.chosen_fields[config['name']] = dropdown

        if config.get('change_widgets'):
            dropdown.currentIndexChanged.connect(
                lambda index: self.__update_dependent_layouts(
                    config['name'],
                    dropdown.itemText(index)
                )
            )
        return dropdown

    def __get_widget_pos(
        self,
        current_row: int,
        current_col: int,
        col_amount: int,
        widget_pos: str = None
    ) -> tuple:
        positions = {
            "first": 0,
            "last": col_amount - 1,
            "current": current_col
        }
        if current_col == col_amount:
            current_row += 1
            current_col = 0

        if widget_pos:
            if widget_pos == "first":
                if current_col > 0:
                    current_row += 1
                return current_row, positions['first']

            if widget_pos == "current":
                return current_row, current_col

            if widget_pos == "last":
                return current_row, positions['last']

            if widget_pos == "middle":
                if current_col < (col_amount - 1) // 2:
                    current_col = (col_amount - 1) // 2
                return current_row, current_col

        return current_row, current_col

    def __update_dependent_layouts(self, name, selected_value):

        self.current_changing_value = selected_value
        if name not in self.dependencies:
            return
        for layout_name, layout in self.dependencies[name].items():
            parent_layout = layout.parentWidget().layout()
            if not parent_layout:
                continue
            position = parent_layout.indexOf(layout)
            if position == -1:
                continue
            self.remover.delete_layout(parent_layout, layout)

            # Ищем новую конфигурацию для этого layout
            new_layout_config = self.finder.find_layout_by_name(
                self.config["layout"]["widgets"],
                layout_name
            )
            if not new_layout_config:
                continue  # Если конфигурация не найдена, пропускаем

            new_layout = self.__create_layout(new_layout_config)
            self.__add_widgets(
                new_layout,
                new_layout_config["type"],
                new_layout_config["widgets"],
                new_layout_config.get("columns")
            )

            # Вставляем новый контейнер на старое место
            parent_layout.insertLayout(position, new_layout)
            self.dependencies[name][layout_name] = new_layout

    def __check_if_widget_is_active(self, config):
        if (
            config.get('active_when') and
            self.current_changing_value and
            self.current_changing_value not in config['active_when']
        ):
            return False
        return True
