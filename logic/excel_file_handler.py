import os
import win32com.client as win32

from decimal import Decimal, ROUND_HALF_UP

from settings import settings as set


class ExcelFileHandler:
    def __init__(self, part_of_the_shelf, data):
        self.part_of_the_shelf = part_of_the_shelf
        self.data = data
        self.worksheet = None

    def prepare_data_for_excel(self):
        if self.part_of_the_shelf.lower() == "travi":
            self.worksheet = "Listino Travi"
            match self.data['Tipo']:
                case "TG":
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

        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Запуск в фоновом режиме
        # excel.DisplayAlerts = False

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

        value_e4 = sheet.Range("E4").Value
        value_e6 = sheet.Range("E6").Value

        if value_e4 > 0:
            value_e4 = Decimal(value_e4).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
            value_e6 = Decimal(value_e6).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        else:
            value_e4 = None
            value_e6 = None

        wb.Close(SaveChanges=False)
        excel.Quit()

        return value_e4, value_e6
