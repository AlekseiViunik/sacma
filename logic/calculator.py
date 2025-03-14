from helpers.helper import Helper


class Calculator:
    def __init__(self, data, type) -> None:
        self.data: dict = data
        self.type: str = type
        self.calc_file_path = Helper.get_calculation_file(self.type)

    def calc_data(self):
        pass
