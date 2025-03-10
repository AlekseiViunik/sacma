from decimal import Decimal
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log
from abstract_base_type import AbstractBaseType


class Grigliato(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self) -> None:
        """
        Метод обработки данных, указанных полльзователем.
        1. Преобразует entries в словарь.
        2. Определяет ячейки вывода.
        3. Создает объект ExcelFileHandler.
        4. Вызывает метод process_excel у созданного объекта.
        5. Считает итоговую стоимость.
        6. Открывает окно с результатами.
        """
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        data = self.type_choice["choices"][entries_dict["Tipo"]]
        rules = data["rules"]
        worksheet = data["worksheet"]
        cells_output = self.evaluate_output_cells(
            data["cells_output"],
            entries_dict
        )
        log.info(f"Entries: {entries_dict}")
        excel = ExcelFileHandler(
            entries_dict,
            rules,
            worksheet,
            cells_output=cells_output,
        )
        excel_data = excel.process_excel()

        cost, weight = self.calculate_total_cost(
            excel_data["price"],
            excel_data["weight"],
            entries_dict["Lunghezza"]
        ) if excel_data["price"] and excel_data["weight"] else (None, None)

        excel_data["price"] = cost
        excel_data["weight"] = weight

        if entries_dict['Base'] == "270x40":
            excel_data["price"] = None
            excel_data["weight"] = None
            self.open_response_window(
                excel_data,
                "ATTENZIONE: Per la base 270x40 contatare la sede!"
            )
        else:
            self.open_response_window(
                excel_data,
                "ATTENZIONE: Per grandi quantitativi contatare la sede!"
            )

    def evaluate_output_cells(
        self,
        cells_output: dict,
        entries_dict: dict
    ) -> dict:
        """
        Метод для вычисления ячеек вывода.

        Parameters
        ----------
            cells_output : dict
                словарь с ячейками вывода.
            entries_dict : dict
                словарь с данными, введенными пользователем.

        Return
        ------
            cells_output : dict
                словарь с вычисленными ячейками вывода.
        """
        cells = {
            "price": cells_output[
                entries_dict["Base"]
            ][entries_dict["Spessore"]]["price"],
            "weight": cells_output[
                entries_dict["Base"]
            ][entries_dict["Spessore"]]["weight"],
        }
        return cells

    def calculate_total_cost(
        self,
        cost_m: Decimal,
        weight_m: Decimal,
        length
    ) -> tuple:
        """Метод для вычисления общей стоимости и веса.

        Parameters
        ----------
            cost_m : Decimal
                стоимость за метр.
            weight_m : Decimal
                вес за метр.
            length : Decimal
                длина.

        Return
        ------
            cost : Decimal
                общая стоимость.
            weight : Decimal
                общий вес.
        """
        cost = cost_m * int(length) / 1000
        weight = weight_m * int(length) / 1000
        return cost, weight
