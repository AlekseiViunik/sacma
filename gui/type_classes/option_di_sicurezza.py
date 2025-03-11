import re

from decimal import Decimal

from abstract_base_type import AbstractBaseType
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log


class OptionDiSicurezza(AbstractBaseType):
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

        # Преобразуем введенные значения в словарь
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        data = self.type_choice['choices'][entries_dict['tipo']]
        rules = data['available_params']['rules']
        worksheet = data['worksheet']
        cells_output = self.__evaluate_output_cells(
            data['available_params']['cells_output'],
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

        excel_data = self.__get_total_price_and_weight(excel_data)

        if entries_dict['tipo'] in ["TESTATE", "PARACOLPI"]:
            self.open_response_window(
                excel_data,
                "ATTENZIONE: Tasselli non inclusi!"
            )
        elif entries_dict['tipo'] == "GUARDRAIL":
            self.open_response_window(
                excel_data,
                "ATTENZIONE: Tasselli e bulloni non inclusi!"
            )

    def __evaluate_output_cells(
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
                словарь с вычисленными адресами ячеек вывода.
        """
        cells = {
            "price": cells_output[
                entries_dict['tipo elemento']
            ]['price'],
            "weight": cells_output[
                entries_dict['tipo elemento']
            ]['weight'],
        }
        if (
            "Inviti inclinati?" in entries_dict.keys() and
            entries_dict["Inviti inclinati?"] != "Sì"
        ):
            cells["additional_price"] = "B28"
            cells["additional_weight"] = "D28"
        return cells

    def __get_total_price_and_weight(self, excel_data: dict) -> dict:
        price = []
        weight = []
        keys = []
        for key, value in excel_data.items():
            if "price" in key:
                price.append(value)
            elif "weight" in key:
                if value.isnumeric():
                    weight.append(Decimal(value))
                else:
                    match = re.search(r'\d+[.,]?\d*', value)
                    if match:
                        number_str = match.group().replace(",", ".")
                    weight.append(Decimal(number_str))
            else:
                continue
            keys.append(key)
        for key in keys:
            excel_data.pop(key)
        if price:
            excel_data["price"] = sum(price)
        if weight:
            excel_data["weight"] = sum(weight)
        return excel_data
