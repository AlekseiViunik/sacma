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
        if keys:
            self.calc_config = Helper.get_nested_data(
                keys,
                self.calc_config
            )
        else:
            self.calc_config = self.calc_config['choices']

        if self.calc_config.get('special_output'):
            self.calc_config.pop('special_output')
            keys = list(self.data.values())
            self.calc_config['cells_output'] = Helper.get_nested_data(
                keys,
                self.calc_config['cells_output']
            )

        post_message = self.calc_config['cells_output'].pop(
            'post_message',
            None
        )
        is_hide = self.calc_config['cells_output'].pop(
            'hide',
            None
        )
        self.translated_data = Translator.translate_dict(self.data)
        self.excel_handler = ExcelHandler(
            self.translated_data,
            self.calc_config['rules'],
            self.calc_config['worksheet'],
            self.calc_config['cells_input'],
            self.calc_config['cells_output']
        )
        excel_result = self.excel_handler.initiate_process()
        if excel_result.get('error'):
            post_message = excel_result.pop('error')
        else:
            if self.calc_config.get('formulas'):
                self.__use_formula(
                    excel_result,
                    self.calc_config['formulas'],
                    self.data
                )

        # Устанавливаем реультат как None, если его не нужно
        # отображать (is_hide = 1)
        excel_result = {
            k: None if is_hide else v for k, v in excel_result.items()
        }

        return excel_result, post_message

    def __use_formula(self, output_dict, formulas, imput_dict={}):
        merged_dicts = Helper.merge_numeric_dicts(output_dict, imput_dict)
        for formula_name, formula in formulas.items():
            if output_dict[formula_name]:
                result = FormulasHandler().apply_formula(
                    merged_dicts,
                    formula,
                    formula_name
                )
            output_dict[formula_name] = result
