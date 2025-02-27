import inspect
import os
import win32com.client as win32

from decimal import Decimal, ROUND_HALF_UP

from logic.logger import logger as log
from logic.validator import Validator
from settings import settings as set


class ExcelFileHandler:
    def __init__(self, part_of_the_shelf, data):
        self.part_of_the_shelf = part_of_the_shelf
        self.data = data
        self.worksheet = None

    def prepare_data_for_excel(self):
        # TODO Добавить докстринги

        log.info("Prepare data to insert it in excel")

        if self.part_of_the_shelf.lower() == "travi":
            if not self.check_data(
                set.TRAVI_RULES[self.data[set.TRAVI_TYPE_KEY]]
            ):
                log.error("The data is wrong!")
                return None

            self.worksheet = set.TRAVI_WORKSHEET
            match self.data[set.TRAVI_TYPE_KEY]:
                case set.TRAVI_TYPE_TG:
                    data_prepared = self.prepare_dict(set.TRAVI_CELLS_TG)
                case set.TRAVI_TYPE_APERTE:
                    data_prepared = self.prepare_dict(set.TRAVI_CELLS_APERTE)
                case set.TRAVI_TYPE_SAT:
                    data_prepared = self.prepare_dict(set.TRAVI_CELLS_SAT)
                case set.TRAVI_TYPE_PORTA_SKID:
                    data_prepared = self.prepare_dict(
                        set.TRAVI_CELLS_PORTA_SKID
                    )
            log.info("The data is prepared")
            return data_prepared

    def prepare_dict(self, cells):
        # TODO Добавить докстринги
        log.info("Prepare dictionary where key is cell address")
        data_prepared = {}
        for name, cell in cells.items():
            if name in self.data:
                self.data[name] = self.data[name].replace("=", "").strip()
                data_prepared[cell] = self.data[name]
        log.info(f"Dictionary is prepared: {data_prepared}")
        return data_prepared

    def get_result_cells(self):
        # TODO Переделать на словарь
        # TODO Добавить обработку для других типов полок
        # TODO Добавить докстринги
        log.info("Getting address of the price and weight cells")
        if self.part_of_the_shelf.lower() == set.TRAVI:
            match self.data[set.TRAVI_TYPE_KEY]:
                case set.TRAVI_TYPE_TG:
                    price_cell = set.TRAVI_CELLS_TG[set.PRICE]
                    weight_cell = set.TRAVI_CELLS_TG[set.WEIGHT]
                case set.TRAVI_TYPE_APERTE:
                    price_cell = set.TRAVI_CELLS_APERTE[set.PRICE]
                    weight_cell = set.TRAVI_CELLS_APERTE[set.WEIGHT]
                case set.TRAVI_TYPE_SAT:
                    price_cell = set.TRAVI_CELLS_SAT[set.PRICE]
                    weight_cell = set.TRAVI_CELLS_SAT[set.WEIGHT]
                case set.TRAVI_TYPE_PORTA_SKID:
                    price_cell = set.TRAVI_CELLS_PORTA_SKID[set.PRICE]
                    weight_cell = set.TRAVI_CELLS_PORTA_SKID[set.WEIGHT]
        log.info(f"The price cell is: {price_cell}")
        log.info(f"The weight cell is: {weight_cell}")
        return price_cell, weight_cell

    def process_excel(self):
        """Открывает Excel, записывает данные, сохраняет, затем открывает
        снова, считывает результаты и закрывает файл."""
        log.info(
            f"The metod '{inspect.currentframe().f_code.co_name}' is called"
        )

        # TODO Файл должен в будущем браться из облака и обновляться 1 раз/день
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(BASE_DIR, "..", "files", "listini.xlsx")
        FILE_PATH = os.path.abspath(FILE_PATH)

        # Подготавливаем данные для записи в Excel
        data_prepared = self.prepare_data_for_excel()
        if not data_prepared:
            return None, None

        # Открываем Excel
        log.info("Open excel file")
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Запуск в фоновом режиме
        # Без обновления связей
        wb = excel.Workbooks.Open(FILE_PATH, UpdateLinks=0)

        log.info("Try to unprotect file and worksheet")
        try:
            wb.Unprotect()  # Снимаем защиту с книги
            log.info("File is unprotected.")
            wb.Sheets(self.worksheet).Unprotect()  # Снимаем защиту с листа
            log.info("Worksheet is unprotected.")
        except Exception:
            log.info("Haven't managed to unprotect")
            pass

        sheet = wb.Sheets(self.worksheet)

        log.info("Insert prepared data to the excel worksheet")
        for cell, value in data_prepared.items():
            log.info(
                f"Insert {value} in the {cell} cell of the worksheet"
                f"'{self.worksheet}'"
            )
            sheet.Range(cell).Value = value

        log.info("Refresh table data to recalculate formulas")
        wb.RefreshAll()  # Обновляем связи
        excel.CalculateUntilAsyncQueriesDone()

        price_cell, weight_cell = self.get_result_cells()
        log.info("Getting price and weight")
        price = sheet.Range(price_cell).Value
        weight = sheet.Range(weight_cell).Value

        # TODO Вынести в отдельный метод
        log.info("Rounding up price and weight")
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

        log.info(f"The price is {price}")
        log.info(f"The weight is {weight}")

        wb.Close(SaveChanges=False)
        excel.Quit()

        return price, weight

    def check_data(self, rules):
        # TODO Добавить докстринги
        # TODO Move this method to the Validator
        log.info("Check data before preparing it")
        for key, value in self.data.items():
            key = key.lower()
            log.info(f"Check {key}")
            if key in rules:
                log.info(f"Data to be checked is: {self.data}")
                for rul_key, rul_value in rules[key].items():
                    if not Validator().validate(rul_key, rul_value, value):
                        log.error(f"{key} hasn't passed")
                        return False
        return True
