from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)


class Creator:

    def __init__(self, config, parent_window):
        self.config: dict = config
        self.parent_window = parent_window  # Нужно для закрытия окна
        self.input_fields = {}

    def create_widget_layout(self, window, layout_config) -> QGridLayout:
        if layout_config:
            layout = self.__create_layout(layout_config)
            self.__add_widgets(
                layout,
                layout_config['type'],
                layout_config['widgets'],
                layout_config.get('columns')
            )
        if (
            isinstance(window, QHBoxLayout) or
            isinstance(window, QVBoxLayout) or
            isinstance(window, QGridLayout)
        ):
            window.addLayout(layout)
        else:
            window.setLayout(layout)

    def __add_widgets(
        self,
        layout,
        layout_type,
        widgets_configs,
        columns=None
    ):
        match layout_type:
            case "grid":
                current_row = 0
                current_column = 0
                for widget_config in widgets_configs:
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
                    self.__create_widget(widget_config, layout)

    def __create_widget(self, config, layout=None, row=None, column=None):
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
                case _:
                    widget = None
            if row is not None and column is not None:
                layout.addWidget(widget, row, column)
            else:
                layout.addWidget(widget)

    def __create_layout(self, layout_config):
        match layout_config["type"]:
            case "grid":
                return QGridLayout()
            case "vertical":
                return QVBoxLayout()
            case "horizontal":
                return QHBoxLayout()
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
        return button

    def __get_widget_pos(
        self,
        current_row: int,
        current_col: int,
        col_amount: int,
        widget_pos: str = None
    ):
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
        return current_row, current_col
