import os
import win32com.client as win32

from decimal import Decimal, ROUND_HALF_UP

from logic.validator import Validator
from settings import settings as set


class ExcelFileHandler:
    def __init__(self, part_of_the_shelf, data):
        self.part_of_the_shelf = part_of_the_shelf
        self.data = data
        self.worksheet = None

    def prepare_data_for_excel(self):
        if self.part_of_the_shelf.lower() == "travi":
            if not self.check_data(
                set.TRAVI_RULES[self.data[set.TRAVI_TYPE_KEY]]
            ):
                return None

            self.worksheet = set.TRAVI_WORKSHEET
            match self.data[set.TRAVI_TYPE_KEY]:
                case set.TRAVI_TYPE_TG:
                    data_prepared = self.prepare_dict(set.TRAVI_CELLS_TG)
            return data_prepared

    def prepare_dict(self, cells):
        data_prepared = {}
        for name, cell in cells.items():
            if name in self.data:
                self.data[name] = self.data[name].replace("=", "").strip()
                data_prepared[cell] = self.data[name]
        return data_prepared

    def process_excel(self):
        """Открывает Excel, записывает данные, сохраняет, затем открывает
        снова, считывает результаты и закрывает файл."""

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(BASE_DIR, "..", "files", "listini.xlsx")
        FILE_PATH = os.path.abspath(FILE_PATH)

        data_prepared = self.prepare_data_for_excel()
        if not data_prepared:
            return None, None

        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Запуск в фоновом режиме

        wb = excel.Workbooks.Open(FILE_PATH, UpdateLinks=0)

        try:
            wb.Unprotect()  # Снимаем защиту с книги
            wb.Sheets("Listino Travi").Unprotect()  # Снимаем защиту с листа
        except Exception:
            pass

        sheet = wb.Sheets("Listino Travi")

        for cell, value in data_prepared.items():
            sheet.Range(cell).Value = value

        wb.RefreshAll()  # Обновляем связи
        excel.CalculateUntilAsyncQueriesDone()

        price = sheet.Range("E4").Value
        weight = sheet.Range("E6").Value

        if price > 0:
            price = Decimal(price).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
            weight = Decimal(weight).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        else:
            price = None
            weight = None

        wb.Close(SaveChanges=False)
        excel.Quit()

        return price, weight

    def check_data(self, rules):
        for key, value in self.data.items():
            key = key.lower()
            if key in rules:
                for rul_key, rul_value in rules[key].items():
                    if not Validator().validate(rul_key, rul_value, value):
                        return False
        return True
