
from logic.excel_file_handler import ExcelFileHandler
from logic.logger import logger as log
from abstract_base_type import AbstractBaseType


class Travi(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self):
        entries_dict = {
            key: entry.get() for key, entry in self.entries.items()
        }
        log.info(f"Entries: {entries_dict}")
        excel = ExcelFileHandler(self.type, entries_dict)
        cost, weight = excel.process_excel()
        self.open_response_window(cost, weight)
