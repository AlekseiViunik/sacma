from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton
)


class Creator:

    def __init__(self, config, parent_window):
        self.config: dict = config
        self.parent_window = parent_window  # Нужно для закрытия окна
        self.input_fields = {}

    def create_window_layout(self) -> QGridLayout:
        grid_layout = QGridLayout()
        if self.config:
            for row in self.config.keys():
                if "row_" in row:
                    row_num = int(row[4:])
                    for column, widget_config in self.config[row].items():
                        column_num = int(column[7:])
                        widget = self.__create_widget(
                            widget_config,
                        )
                        grid_layout.addWidget(widget, row_num, column_num)
        return grid_layout

    def __create_widget(self, config):
        match config['type']:
            case "label":
                widget = self.__create_label(config)
            case "input":
                widget = self.__create_input(config)
            case "button":
                widget = self.__create_button(config)
            case _:
                widget = None
        return widget

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
