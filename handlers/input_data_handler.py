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

