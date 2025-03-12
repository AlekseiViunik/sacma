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
                            row_num,
                            column_num
                        )
                        grid_layout.addWidget(widget, row_num, column_num)
        return grid_layout

    def __create_widget(self, config, row, column):
        match config["type"]:
            case "label":
                widget = self.__create_label(config)
            case "input":
                widget = self.__create_input(config, row, column)
            case "button":
                widget = self.__create_button(config)
            case _:
                widget = None
        return widget

    def __create_label(self, config: dict) -> QLabel:
        return QLabel(config["text"])

    def __create_input(self, config: dict, row, column) -> QLineEdit:
        input_field = QLineEdit()
        for param, value in config.items():
            match param:
                case "width":
                    input_field.setFixedWidth(int(value))
                case "height":
                    input_field.setFixedHeight(int(value))
                case "default_value":
                    input_field.setPlaceholderText(value)
        self.input_fields[f"{row}.{column}"] = input_field
        return input_field

    def __create_button(self, config: dict) -> QPushButton:
        button = QPushButton(config["text"])
        for param, value in config.items():
            match param:
                case "width":
                    button.setFixedWidth(int(value))
                case "height":
                    button.setFixedHeight(int(value))
                case "callback":
                    self.__connect_callback(
                        button,
                        value,
                        config.get("params", {})
                    )
        return button

    def __connect_callback(self, button, callback_name, params):
        if callback_name == "close_window" and self.parent_window:
            button.clicked.connect(self.parent_window.close)
        elif callback_name == "browse_file":
            target_input = params.get("target_input")
            button.clicked.connect(lambda: self.__browse_file(target_input))
        elif callback_name == "save_settings":
            button.clicked.connect(self.__save_settings)

    def __browse_file(self, target_input):
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Выбрать файл",
            "",
            "Excel Files (*.xlsx *.xls)"
        )
        if file_path and target_input in self.input_fields:
            self.input_fields[target_input].setText(file_path)

    def __save_settings(self):
        import json
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    key: field.text()
                    for key, field in self.input_fields.items()
                },
                f, indent=4, ensure_ascii=False
            )
        if self.parent_window:
            self.parent_window.close()
