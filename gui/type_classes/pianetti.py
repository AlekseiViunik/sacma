from abstract_base_type import AbstractBaseType
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log


class Pianetti(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self) -> None:
        """Метод обработки данных, указанных полльзователем.
        1. Преобразует entries в словарь.
        2. Создает объект ExcelFileHandler.
        3. Вызывает метод process_excel у созданного объекта.
        4. Открывает окно с результатами.
        """
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        data = self.type_choice["choices"]["standart"]
        rules = data["rules"]
        worksheet = data["worksheet"]
        cells_input = data["cells_input"]
        cells_output = data["cells_output"]
        log.info(f"Entries: {entries_dict}")
        excel = ExcelFileHandler(
            entries_dict,
            rules,
            worksheet,
            cells_input,
            cells_output
        )
        excel_data = excel.process_excel()
        self.open_response_window(excel_data)
