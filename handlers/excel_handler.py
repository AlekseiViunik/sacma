from decimal import Decimal, ROUND_HALF_UP
import win32com.client as win32

from logic.translator import Translator
from logic.logger import logger as log
from logic.validator import Validator
from handlers.json_handler import JsonHandler

SETTINGS_FILE = "settings.json"


class ExcelHandler:
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
        self.settings_json_handler = JsonHandler(SETTINGS_FILE)
        self.excel = None
        self.wb = None
        self.sheet = None
        self.check_err_mesg = ""

    def initiate_process(self):
        if not self.__check_data():
            log.error("The data is wrong!")
            return {
                "price": None,
                "weight": None,
                "error": self.check_err_mesg
            }

        self.excel, self.wb, self.sheet = self.__open_excel()
        self.__input_cells()
        return self.__get_data_from_excel()

    def __open_excel(self):

        file_path = self.settings_json_handler.get_value_by_key('excel_path')

        log.info("Open excel file")
        try:
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = False  # Запуск в фоновом режиме
            log.info(f"File path is {file_path}")
        except Exception as e:
            log.error(f"Ошибка при запуске Excel: {e}")
        log.info("Excel is opened")
        # Без обновления связей
        try:
            wb = excel.Workbooks.Open(file_path, UpdateLinks=0)
            log.info("Excel is opened")
        except Exception as e:
            log.error(f"Didn't manage to open excel: {e}")

        return excel, wb, wb.Sheets(self.worksheet)

    def __input_cells(self):
        if self.cells_input:
            # Подготавливаем данные для записи в Excel
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
                self.sheet.Range(cell).Value = value

            log.info("Refresh table data to recalculate formulas")
            self.wb.RefreshAll()  # Обновляем связи
            self.excel.CalculateUntilAsyncQueriesDone()

    def __check_data(self) -> bool:
        """
        Используя валидатор проверяет данные согласно определенным правилам,
        указанным в файле настроек.

        Returns
        -------
        bool
            Результат валидации данных.
        """
        log.info("Check data before preparing it")
        for key, value in self.data.items():
            key = key.capitalize()
            log.info(f"Check {key}")
            if key in self.rules:
                log.info(f"Data to be checked is: {self.data}")
                for rule_key, rule_value in self.rules[key].items():
                    if not Validator().validate(rule_key, rule_value, value):
                        self.check_err_mesg = self.set_err_msg(
                            rule_key,
                            rule_value,
                            key,
                            value
                        )
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

    def __get_data_from_excel(self) -> dict:
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
            key: self.sheet.Range(self.cells_output[key]).Value
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

    def set_err_msg(
        self,
        rule_key,
        rule_value,
        key,
        value
    ):
        match rule_key:
            case "min":
                return (
                    f"{key} should be more than {rule_value}. You have {value}"
                )
            case "max":
                return (
                    f"{key} should be less than {rule_value}. You have {value}"
                )
            case "numeric":
                return (
                    f"{key} should be numeric. You have {value}"
                )
            case "natural":
                return (
                    f"{key} should be more positive and numeric."
                    f"You have {value}"
                )
            case "multiple":
                return (
                    f"{key} should be multiple {rule_value}. You have {value}"
                )
            case _:
                return ""
