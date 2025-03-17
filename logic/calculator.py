from handlers.excel_handler import ExcelHandler
from handlers.formulas_handler import FormulasHandler
from handlers.json_handler import JsonHandler
from helpers.helper import Helper
from logic.translator import Translator


class Calculator:
    def __init__(self, data, type, choices) -> None:
        self.data: dict = data
        self.type: str = type
        self.choices: dict = choices
        self.calc_file_path: str = Helper.get_calculation_file(self.type)
        self.calc_config: dict = {}
        self.config_file_handler = JsonHandler(self.calc_file_path)
        self.excel_handler: ExcelHandler | None = None

    def calc_data(self):
        self.calc_config = self.config_file_handler.get_all_data()
        keys = list(self.choices.values())
        self.calc_config = self.calc_config = Helper.get_nested_data(
            keys,
            self.calc_config
        )
        self.data = Translator.translate_dict(self.data)
        self.excel_handler = ExcelHandler(
            self.data,
            self.calc_config['rules'],
            self.calc_config['worksheet'],
            self.calc_config['cells_input'],
            self.calc_config['cells_output']
        )
        excel_result = self.excel_handler.initiate_process()

        if self.calc_config.get('formulas'):
            self.__use_formula(
                excel_result,
                self.calc_config['formulas']
            )

        return excel_result

    def __use_formula(self, data, formulas):

        for formula_name, formula in formulas.items():
            if data[formula_name]:
                result = FormulasHandler().apply_formula(data, formula)
            data[formula_name] = result
