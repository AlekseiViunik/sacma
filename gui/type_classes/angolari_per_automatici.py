from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log
from abstract_base_type import AbstractBaseType


class AngolariPerAutomatici(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self) -> None:
        """
        Метод обработки данных, указанных полльзователем.
        1. Преобразует entries в словарь.
        2. Создает объект ExcelFileHandler.
        3. Вызывает метод process_excel у созданного объекта.
        4. Открывает окно с результатами.
        """
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        data = self.type_choice["choices"][entries_dict["pattini"]]
        rules = data["rules"]
        worksheet = data["worksheet"]
        cells_input = data["cells_input"]
        cells_output = data["cells_output"]
        log.info(f"Entries: {entries_dict}")
        excel = ExcelFileHandler(
            entries_dict,
            rules,
            worksheet,
            cells_input=cells_input,
            cells_output=cells_output,
        )
        excel_data = excel.process_excel()
        self.open_response_window(excel_data)

    # def calculate_total_cost(
    #     self,
    #     cost_m: Decimal,
    #     weight_m: Decimal,
    #     length
    # ) -> tuple:
    #     """Метод для вычисления общей стоимости и веса.
    #
    #     Parameters
    #     ----------
    #         cost_m : Decimal
    #             стоимость за метр.
    #         weight_m : Decimal
    #             вес за метр.
    #         length : Decimal
    #             длина.
    #
    #     Return
    #     ------
    #         cost : Decimal
    #             общая стоимость.
    #         weight : Decimal
    #             общий вес.
    #     """
    #     cost = cost_m * int(length) / 1000
    #     weight = weight_m * int(length) / 1000
    #     return cost, weight
