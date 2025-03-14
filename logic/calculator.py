from handlers.json_handler import JsonHandler
from helpers.helper import Helper


class Calculator:
    def __init__(self, data, type, choices) -> None:
        self.data: dict = data
        self.type: str = type
        self.choices: dict = choices
        self.calc_file_path: str = Helper.get_calculation_file(self.type)
        self.calc_config: dict = {}
        self.config_file_handler = JsonHandler(self.calc_file_path)

    def calc_data(self):
        self.calc_config = self.config_file_handler.get_all_data()
        keys = list(self.choices.values())
        self.calc_config = self.calc_config = Helper.get_nested_data(
            keys,
            self.calc_config
        )
        pass
