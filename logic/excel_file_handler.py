import inspect
import os
import sys
import win32com.client as win32

from decimal import Decimal, ROUND_HALF_UP

from logic.logger import logger as log
from logic.translator import Translator
from logic.validator import Validator


class ExcelFileHandler:
    """
    Обработчик файлов Excel. Подгатавливает и отправляет данные,
    выбранные/введенные юзером и возвращает результат.

    Attributes
    ----------
    data : dict
        Значения полей выбранные/введенные юзером.
    rules : dict
        Правила валидации выбранных/введенных данных.
    worksheet : str
        Имя листа excel, где будут вбиваться данные и получаться результат.
    cells_input : dict | None, optional
        Соответствие имен лейблов для которых юзер вводил данные номерам
        ячеек, куда эти данные должны быть вставлены.
    cells_output : dict | None, optional
        Соответствие имен лейблов окна результата номерам ячеек, где
        находится результат.

    Methods
    -------
    process_excel()
        Открывает файл excel. Вызывает методы подготовки данных.
        Проверяет вводимые данные. Получает расчитанный результат.
    """

    def __init__(
        self,
        data: dict,
        rules: dict,
        worksheet: str,
        cells_input: dict | None = None,
        cells_output: dict | None = None
    ) -> None:
        self.data = data
        self.rules: dict | None = (
            Translator().translate_dict(rules)
        )
        self.worksheet = worksheet
        self.cells_input: dict | None = (
            Translator().translate_dict(cells_input)
            if cells_input
            else None
        )
        self.cells_output: dict = cells_output

    def process_excel(self) -> dict:
        """
        Основной метод класса ExcelFileHandler. Открывает файл, записывает в
        него данные (предварительно вызвав методы подготовки данных), обновляет
        расчеты файла, получает цену и вес элемента шкафа, необходимые нам,
        округляет и возвращает их. Также проводим валидацию данных.

        Returns
        -------
        data : dict
            Словарь с ценой и весом (в будущем могут быть так же другие данные)
        """

        log.info(
            f"The metod '{inspect.currentframe().f_code.co_name}' is called"
        )

        # TODO Файл должен в будущем браться из облака и обновляться 1 раз/день
        # Определяем, где находится исполняемый файл (или скрипт)
        if getattr(sys, "frozen", False):  # Если запущено как .exe
            BASE_DIR = os.path.dirname(sys.executable)
            FILE_PATH = os.path.join(BASE_DIR, "files", "listini.xlsx")
        else:  # Если запущено как .py
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            FILE_PATH = os.path.join(BASE_DIR, "..", "files", "listini.xlsx")
        FILE_PATH = os.path.abspath(FILE_PATH)

        log.info("Check data before insert it in excel")
        # Проверяем данные перед вставкой в excel
        if not self.__check_data():
            log.error("The data is wrong!")
            return {"price": None, "weight": None}

        # Открываем Excel
        log.info("Open excel file")
        try:
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False  # Запуск в фоновом режиме
            log.info(f"File path is {FILE_PATH}")
        except Exception as e:
            log.error(f"Ошибка при запуске Excel: {e}")

        log.info("Excel is opened")
        # Без обновления связей
        try:
            wb = excel.Workbooks.Open(FILE_PATH, UpdateLinks=0)
            log.info("Excel is opened")
        except Exception as e:
            log.error(f"Didn't manage to open excel: {e}")

        sheet = wb.Sheets(self.worksheet)

        if self.cells_input:
            # Подготавливаем данные для записи в Excel
            if self.cells_input:
                data_prepared = self.__prepare_data()
                if not data_prepared:
                    return None, None
            # Вставляем данные в Excel
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

        data = self.__get_data_from_excel(sheet)
        # Закрываем файл без сохранения
        log.info("Close the file without saving")
        wb.Close(SaveChanges=False)
        excel.Quit()
        log.info("File is closed")

        return data

# ============================ Приватные методы ===============================

    def __check_data(self) -> bool:
        """
        Используя валидатор проверяет данные согласно определенным правилам,
        указанным в файле настроек.

        Returns
        -------
        bool
            Результат валидации данных.
        """
        # TODO Перенести эту проверку в Валидатор
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
        log.info("The data is correct")
        return True

    def __prepare_data(self) -> dict:
        """
        В имеющемся эксель файлы есть варианты <1000 и >1001. Это не совсем
        логично, поэтому я заменил эти варианты для выбора пользователем на
        более логичные <=1000 и >= 1001. Однако такой вариант не подойдет для
        формул excel, которые я не могу поменять и поэтому явным образом в этом
        методе удаляем у полей, которых это касается знаки '='. Также
        преобразуем в словарь tk.Entry.

        Returns
        -------
        data_prepared : dict
            Отвалидированные и подготовленные для дальнейшей обработки данные.
        """

        log.info("Prepare dictionary where key is cell address")

        # Подготавливаем данные для записи в Excel
        data_prepared = {}
        for name, cell in self.cells_input.items():
            if name in self.data.keys():
                if isinstance(self.data[name], str):
                    self.data[name] = self.data[name].replace("=", "").strip()
                data_prepared[cell] = self.data[name]
        log.info(f"Dictionary is prepared: {data_prepared}")
        return data_prepared

    def __get_data_from_excel(self, sheet) -> dict:
        """
        Получаем и округляем цену и вес из таблицы excel.
        При необходимости получаем и другие данные.

        Parameters
        ----------
        sheet : win32.Dispatch.Workbooks.Sheets
            Текущий лист excel.

        Returns
        -------
        excel_data : dict
            Словарь полученными из excel данными.
        """
        log.info("Getting excel data")
        excel_data = {
            key: sheet.Range(self.cells_output[key]).Value
            for key in self.cells_output
        }

        # Округляем
        log.info("Rounding up data")
        for key, value in excel_data.items():
            if (
                value and
                str(value).replace(".", "", 1).isdigit() and
                float(value) > 0
            ):
                excel_data[key] = Decimal(value).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )
        return excel_data
