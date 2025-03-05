import inspect
import os
import tkinter as tk
import win32com.client as win32

from decimal import Decimal, ROUND_HALF_UP

from logic.logger import logger as log
from logic.translator import Translator
from logic.validator import Validator
from typing import Dict, Tuple, Any


class ExcelFileHandler:
    """Обработчик файлов Excel. Подгатавливает и отправляет данные,
    выбранные/введенные юзером и возвращает результат.

    Attributes
    ----------
        part_of_the_shelf : str
            Элемент шкафа, для которого будет проводиться расчет цены
        data : List[tk.Entry]
            Список данных, выбранных/введенных юзером.
        worksheet : str
            Имя листа excel, где будут вбиваться данные и получаться результат.

    Methods
        -------
            prepare_data_for_excel()
                Вызывает проверку данных. Вызывает преобразование данных в
                словарь.
            prepare_dict(cells)
                Преобразует tk.Entry в словарь. УБирает знаки, которые
                отсутствуют в файле excel.
            get_result_cells()
                Получает адреса ячеек excel, в которых содержится результат.
            process_excel()
                Открывает файл excel. Вызывает методы подготовки данных.
                Получает и округляет результат.
            check_data(rules)
                На основании заранее определенных правил проверяет данные перед
                преобразованием их в словарь.
    """

    def __init__(
        self,
        data: tk.Entry,
        rules: Dict,
        worksheet: str | None,
        cells_input: Dict[str, str],
        cells_output: Dict[str, str]
    ) -> None:
        self.data: tk.Entry = data
        self.worksheet: str | None = None
        self.rules = Translator().translate_dict(rules)
        self.cells_input = Translator().translate_dict(cells_input)
        self.cells_output = cells_output
        self.worksheet = worksheet

    def prepare_data(self) -> Dict[str, Any] | None:
        """В имеющемся эксель файлы есть варианты <1000 и >1001. Это не совсем
        логично, поэтому я заменил эти варианты для выбора пользователем на
        более логичные <=1000 и >= 1001. Однако такой вариант не подойдет для
        формул excel, которые я не могу поменять и поэтому явным образом в этом
        методе удаляем у полей, которых это касается знаки '='. Также
        преобразуем в словарь tk.Entry.

        Parameters
        __________
            cells : Dict[str, str]
                Массив хранящий соответствие имен лейблов для которых юзер
                вводил данные номерам ячеек, куда эти данные должны быть
                вставлены.

        Return
        ______
            data_prepared : Dict[str, Any] | None
                Преобразованные в словарь данные.
        """
        log.info("Check data before insert it in excel")
        # Проверяем данные перед вставкой в excel
        if not self.check_data():
            log.error("The data is wrong!")
            return None

        log.info("The data is correct")
        log.info("Prepare dictionary where key is cell address")

        # Подготавливаем данные для записи в Excel
        data_prepared = {}
        for name, cell in self.cells_input.items():
            if name in self.data:
                self.data[name] = self.data[name].replace("=", "").strip()
                data_prepared[cell] = self.data[name]
        log.info(f"Dictionary is prepared: {data_prepared}")
        return data_prepared

    def process_excel(self) -> Tuple[Decimal, Decimal]:
        """Основной метод класса ExcelFileHandler. Открывает файл, записывает в
        него данные (предварительно вызвав методы подготовки данных), обновляет
        расчеты файла, получает цену и вес элемента шкафа, необходимые нам,
        округляет и возвращает их.

        Return
        ______
            price : Decimal
                Цена элемента шкафа.
            wight : Decimal
                Вес элемента шкафа.
        """

        log.info(
            f"The metod '{inspect.currentframe().f_code.co_name}' is called"
        )

        # TODO Файл должен в будущем браться из облака и обновляться 1 раз/день
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FILE_PATH = os.path.join(BASE_DIR, "..", "files", "listini.xlsx")
        FILE_PATH = os.path.abspath(FILE_PATH)

        # Подготавливаем данные для записи в Excel
        data_prepared = self.prepare_data()
        if not data_prepared:
            return None, None

        # Открываем Excel
        log.info("Open excel file")
        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False  # Запуск в фоновом режиме

        # Без обновления связей
        wb = excel.Workbooks.Open(FILE_PATH, UpdateLinks=0)

        log.info("Try to unprotect file and worksheet")

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

        log.info("Getting price and weight")
        price = sheet.Range(self.cells_output["price"]).Value
        weight = sheet.Range(self.cells_output["weight"]).Value

        # Округляем цену и вес
        log.info("Rounding up price and weight")
        if price > 0:
            price, weight = (Decimal(unit).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            ) for unit in [price, weight])
        else:
            price = None
            weight = None

        log.info(f"The price is {price}")
        log.info(f"The weight is {weight}")

        # Закрываем файл без сохранения
        log.info("Close the file without saving")
        wb.Close(SaveChanges=False)
        excel.Quit()
        log.info("File is closed")

        return price, weight

    def check_data(self) -> bool:
        """Используя валидатор проверяет данные согласно определенным правилам,
        указанным в файле настроек.

        Parameters
        __________
            rules : Dict[str: Dict[str: Any]]
                Массив с набором правил валидации.

        Return
        ______
            result : bool
                Результат валидации данных.
        """
        # TODO Move this method to the Validator
        log.info("Check data before preparing it")
        for key, value in self.data.items():
            key = key.capitalize()
            log.info(f"Check {key}")
            if key in self.rules:
                log.info(f"Data to be checked is: {self.data}")
                for rul_key, rul_value in self.rules[key].items():
                    if not Validator().validate(rul_key, rul_value, value):
                        log.error(f"{key} hasn't passed")
                        return False
        return True
