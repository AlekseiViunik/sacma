from PyQt6.QtWidgets import (
    QMessageBox
)

from helpers.remover import Remover


class InputDataHandler:
    def __init__(self):
        self.remover = Remover()

    def collect_all_inputs(self, input_fields, choice_fields):
        self.remover.clean_up_fields(
            input_fields,
            choice_fields
        )
        all_inputs = {}
        for name, field in choice_fields.items():
            all_inputs[name] = field.currentText()
        for name, field in input_fields.items():
            all_inputs[name] = field.text()
        return all_inputs

    def check_mandatory(self, inputs, mandatories):
        filled_inputs = {k for k, v in inputs.items() if v}
        return list(set(mandatories) - filled_inputs)

    def show_error_messagebox(self, title, msg, window):
        box = QMessageBox(window)
        box.setWindowTitle(title)
        box.setText(msg)
        box.setIcon(QMessageBox.Icon.Critical)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.show()

    def show_success_messagebox(self, title, msg, window):
        box = QMessageBox(window)
        box.setWindowTitle(title)
        box.setText(msg)
        box.setIcon(QMessageBox.Icon.Information)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.exec()
