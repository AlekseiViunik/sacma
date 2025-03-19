from decimal import Decimal, ROUND_HALF_UP
import win32com.client
import win32com.client as win32

from logic.translator import Translator
from logic.logger import logger as log
from logic.validator import Validator
from handlers.json_handler import JsonHandler

SETTINGS_FILE = "settings.json"


class ExcelHandler:
    """
    Работает с экселем. Открывает/закрывает файлы ексель, вызывает проверку
    данных, готовит и пишет данные в файл, получает данные из файла.

    Attributes
    ----------
    data: dict
        Данные, которые необходимо обработать и записать в файл.

    rules: dict | None
        Правила, по которым будет происходить валидация данных.

    worksheet: str
        Имя листа файла эксель, в который будет происходить запись данных.

    cells_input: dict | None
        Словарь, содержащий данные типа <Имя_поля>: <Адрес_ячейки_для_записи>.

    cells_output: dict
        Словарь с данными типа <Имя_поля>: <Адрес_ячейки_для_извлечения>.

    settings_json_handler: JsonHandler
        Обработчик файла общих настроек. Нужен для получения пути к эксель
        файлу. Путь хранится в общих настройках.

    excel: win32com.client.CDispatch | None
        Объект приложения ексель.

    wb: win32com.client.CDispatch | None
        Объект книги эксель.

    sheet: win32com.client.CDispatch | None
        Объект листа книги эксель.

    check_err_mesg: str
        Сообщение об ошибке, которое будет сформировано в случае, если какие-то
        из данных не пройдут валидацию.

    Methods
    -------
    initiate_process()
        Основной метод класса. Запускает обработку, подготовку и прочие
        действия с файлом и данными.

    Private pethods
    ---------------
    __open_excel()
        Открывает файл эксель.

    __close_excel()
        Закрывает ставший уже ненужным файл эксель.

    __prepare_data()
        Подготавливает данные (см. описание метода) перед вставкой их в эксель.

    __input_cells()
        Вставляет подготовленные данные в эксель и обновляет страницу для
        пересчета формул.

    __check_data()
        Валидирует входные данные согласно правилам изложенным в конфиге окна.

    __get_data_from_excel()
        Извлекает указанные ячейки из файла эксель после пересчета формул и
        возвращает их как результат.

    __set_err_msg(rule_key, rule_value, key, value)
        В случае проваленной валидации данных, формирует сообщение об ошибке в
        зависимости от того, какое правило было провалено.

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
        self.worksheet: str = worksheet
        self.cells_input: dict | None = (
            Translator().translate_dict(cells_input)
            if cells_input
            else None
        )
        self.cells_output: dict | None = cells_output
        self.settings_json_handler: JsonHandler = JsonHandler(SETTINGS_FILE)
        self.excel: win32com.client.CDispatch | None = None
        self.wb: win32com.client.CDispatch | None = None
        self.sheet: win32com.client.CDispatch | None = None
        self.check_err_mesg: str = ""

    def initiate_process(self) -> dict:
        """
        Основной метод класса. Запускает процессы проверки данных,
        открытия/закрытия файла и вставки/получения данных

        Returns
        -------
        data: dict
            Словарь с необработанными данными для вывода в окне результата.
        """

        # Валидация входных данных
        if not self.__check_data():
            log.error("The data is wrong!")
            return {
                "price": None,
                "weight": None,
                "error": self.check_err_mesg
            }

        # Открытие книги и страницы эксель
        self.__open_excel()

        # Запись ячеек в таблицу и пересчет формул
        self.__input_cells()

        # Извлечение пересчитанных ячеек
        data = self.__get_data_from_excel()

        # Закрытие книги и приложения, чтобы не висели в трекере
        self.__close_excel()

        return data

    def __open_excel(self) -> None:
        """
        Открывает файл для работы и обновляет свойства класса, связанные с
        файлом.
        """

        # Получение пути к файлу эксель, который хранится в файле общих
        # настроек
        file_path = self.settings_json_handler.get_value_by_key('excel_path')

        # Попытка запустить приложение
        log.info("Open excel file")
        try:
            self.excel = win32.Dispatch("Excel.Application")
            self.excel.Visible = False  # Запуск в фоновом режиме
            log.info(f"Excel file path is {file_path}")
        except Exception as e:
            log.error(f"Ошибка при запуске Excel: {e}")
        log.info("Excel is opened")

        # Попытка открыть книгу
        try:
            self.wb = self.excel.Workbooks.Open(file_path, UpdateLinks=0)
            log.info("Excel is opened")
        except Exception as e:
            log.error(f"Didn't manage to open excel book: {e}")

        self.sheet = self.wb.Sheets(self.worksheet)

    def __close_excel(self) -> None:
        """
        После работы с файлом, даже когда уже текущее приложение остановлено,
        файл продолжает висеть в задачах и потреблять ресурсы. Этот метод
        принудительно его закрывает.
        """

        log.info("Close excel file")
        # Закрытие книги, если открыта
        if self.wb:
            try:
                self.wb.Close(SaveChanges=0)
            except Exception() as e:
                log.error(f"Error {e}")

        # Закрытие приложения эксель, если открыто
        if self.excel:
            try:
                self.excel.Quit()
            except Exception() as e:
                log.error(f"Error {e}")

    def __prepare_data(self) -> dict:
        """
        В имеющемся эксель файлe есть варианты <1000 и >1001. Это не совсем
        логично, поэтому я заменил эти варианты для выбора пользователем на
        более логичные <=1000 и >= 1001. Однако такой вариант не подойдет для
        формул excel, которые я не могу поменять и поэтому явным образом в этом
        методе удаляем у полей, которых это касается знаки '='.

        Также подготавливаем словарь вида <ячейка_для_вставки>: <значение>,
        который будет использоваться в методе __input_cells() для вставки
        значений.

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
                # Номер ячейки      = Значение переданных данных
                data_prepared[cell] = self.data[name]
        log.info(f"Dictionary is prepared: {data_prepared}")
        return data_prepared

    def __input_cells(self) -> None:
        """
        Вызывает процесс подготовки данных и вписывает их в соответствующие
        ячейки в экселе. После чего обновляет страницу, чтобы пересчитались
        формулы.
        """

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
            # Обновляем связи
            log.info("Refresh table data to recalculate formulas")
            self.wb.RefreshAll()
            self.excel.CalculateUntilAsyncQueriesDone()

    def __check_data(self) -> bool:
        """
        Используя валидатор проверяет данные согласно определенным правилам,
        указанным в конфигурационном файле.

        Пробегаемся по ключам в переданных данных. Если такой ключ есть в
        правилах, то уже пробегаемся по самим правилам и по каждому правилу
        валидируем текущее значение по ключу из данных.

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
                        self.check_err_mesg = self.__set_err_msg(
                            rule_key,
                            rule_value,
                            key,
                            value
                        )
                        log.error(f"{key} hasn't passed")
                        return False
        log.info("The data is correct")
        return True

    def __get_data_from_excel(self) -> dict:
        """
        Получаем и округляем цену и вес из таблицы excel.
        При необходимости получаем и другие данные. Это не всегда финишные
        данные. Возможно им будет нужна обработка.

        Returns
        -------
        excel_data : dict
            Словарь полученными из excel данными.
        """

        log.info("Getting excel data")
        # Получение всех необходимых данных
        excel_data = {
            key: self.sheet.Range(self.cells_output[key]).Value
            for key in self.cells_output
        }

        # Перевод в Децимал и округление.
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

    def __set_err_msg(
        self,
        rule_key,
        rule_value,
        key,
        value
    ) -> str:
        """
        В зависимости от того, какой тип валидации не прошло значение,
        формирует сообщение об ошибке.

        Parameters
        ----------
            rule_key: str
                Имя правила, которое было провалено (например max, min и т.д.).
            rule_value: Any
                Значение правила, которое было не соблюдено.
            key: str
                Имя параметра, значение которого провалило валидацию.
            value: Any
                Знгачение параметра, провалившего валидацию.

        Returns
        -------
        str
            Сообщение об ошибке
        """

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
