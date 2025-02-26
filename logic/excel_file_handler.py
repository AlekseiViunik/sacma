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
        # TODO Добавить докстринги
        # TODO Добавить обработку для других типов полок

        if self.part_of_the_shelf.lower() == "travi":
            if not self.check_data(
                set.TRAVI_RULES[self.data[set.TRAVI_TYPE_KEY]]
            ):
                return None

            self.worksheet = set.TRAVI_WORKSHEET
            match self.data[set.TRAVI_TYPE_KEY]:
                case set.TRAVI_TYPE_TG:
                    data_prepared = self.prepare_dict(set.TRAVI_CELLS_TG)
                case set.TRAVI_TYPE_APERTE:
                    data_prepared = self.prepare_dict(set.TRAVI_CELLS_APERTE)
            return data_prepared

    def prepare_dict(self, cells):
        # TODO Добавить докстринги
        data_prepared = {}
        for name, cell in cells.items():
            if name in self.data:
                self.data[name] = self.data[name].replace("=", "").strip()
                data_prepared[cell] = self.data[name]
        return data_prepared

    def get_result_cells(self):
        # TODO Переделать на словарь
        # TODO Добавить обработку для других типов полок
        # TODO Добавить докстринги
        if self.part_of_the_shelf.lower() == set.TRAVI:
            match self.data[set.TRAVI_TYPE_KEY]:
                case set.TRAVI_TYPE_TG:
                    price_cell = set.TRAVI_CELLS_TG[set.PRICE]
                    weight_cell = set.TRAVI_CELLS_TG[set.WEIGHT]
                case set.TRAVI_TYPE_APERTE:
                    price_cell = set.TRAVI_CELLS_APERTE[set.PRICE]
                    weight_cell = set.TRAVI_CELLS_APERTE[set.WEIGHT]
        return price_cell, weight_cell

    def process_excel(self):
        """Открывает Excel, записывает данные, сохраняет, затем открывает
        снова, считывает результаты и закрывает файл."""

        # TODO Файл должен в будущем браться из облака и обновляться 1 раз/день
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(BASE_DIR, "..", "files", "listini.xlsx")
        FILE_PATH = os.path.abspath(FILE_PATH)

        # Подготавливаем данные для записи в Excel
        data_prepared = self.prepare_data_for_excel()
        if not data_prepared:
            return None, None

        # Открываем Excel
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Запуск в фоновом режиме
        # Без обновления связей
        wb = excel.Workbooks.Open(FILE_PATH, UpdateLinks=0)

        try:
            wb.Unprotect()  # Снимаем защиту с книги
            wb.Sheets(self.worksheet).Unprotect()  # Снимаем защиту с листа
        except Exception:
            pass

        sheet = wb.Sheets(self.worksheet)

        for cell, value in data_prepared.items():
            sheet.Range(cell).Value = value

        wb.RefreshAll()  # Обновляем связи
        excel.CalculateUntilAsyncQueriesDone()
        price_cell, weight_cell = self.get_result_cells()
        price = sheet.Range(price_cell).Value
        weight = sheet.Range(weight_cell).Value

        # TODO Вынести в отдельный метод
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
        # TODO Добавить докстринги
        for key, value in self.data.items():
            key = key.lower()
            if key in rules:
                for rul_key, rul_value in rules[key].items():
                    if not Validator().validate(rul_key, rul_value, value):
                        return False
        return True
