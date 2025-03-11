from abstract_base_type import AbstractBaseType
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log


class Satellitare(AbstractBaseType):
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
        cells_output = self.evaluate_output_cells(
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

        if entries_dict['tipo'] == "AUTOMHA":
            self.open_response_window(
                excel_data,
                "ATTENZIONE: Il prezzo è per metro lineare"
            )
        else:
            self.open_response_window(
                excel_data,
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
                словарь с вычисленными адресами ячеек вывода.
        """
        cells = {
            "price": cells_output[
                entries_dict['Elemento']
            ]['price'],
            "weight": cells_output[
                entries_dict['Elemento']
            ]['weight'],
        }
        return cells
