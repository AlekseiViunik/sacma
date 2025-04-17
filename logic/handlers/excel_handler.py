import gc
import win32com.client
import win32com.client as win32

from typing import Any

from logic.handlers.json_handler import JsonHandler
from logic.preparators.data_preparator import DataPreparator
from settings import settings as sett


class ExcelHandler:
    """
    Работает с экселем. Открывает/закрывает файлы ексель, вызывает проверку
    данных, готовит и пишет данные в файл, получает данные из файла.

    Attributes
    ----------
    - data: dict
        Default = {}\n
        Данные, которые необходимо обработать и записать в файл.

    - rules: dict | None
        Default = None\n
        Правила, по которым будет происходить валидация данных.

    - worksheet: str
        Default = ''\n
        Имя листа файла эксель, в который будет происходить запись данных.

    - cells_input: dict | None
        Default = None\n
        Словарь, содержащий данные типа <Имя_поля>: <Адрес_ячейки_для_записи>.

    - cells_output: dict | None
        Default = None\n
        Словарь с данными типа <Имя_поля>: <Адрес_ячейки_для_извлечения>.

    - copy_cells: dict[str, list[str]] | None
        Default = None\n
        Ячейки, значения которых нужно скопировать в другие ячейки. Ключом
        передается ячейка, которую нужно скопировать. Значением - список ячеек,
        куда нужно скопировать.

    - additional_input: dict[str, Any] | None
        Default = None\n
        Дополнительный ввод, когда у нас есть значения-константы, которые нужно
        ввести в конкретные ячейки, независимо от введенных юзером данных.
        Отображаются в виде словаря {<ячейка>: <данные>}

    - roundings: dict[str, str] | None
        Default = None\n
        Словарь с параметром округления для конкретного поля, если округление
        нестандартное.

    Methods
    -------
    - initiate_process()
        Основной метод класса. Запускает обработку, подготовку и прочие
        действия с файлом и данными.

    - open_excel()
        Открывает файл эксель.

    - close_excel()
        Закрывает ставший уже ненужным файл эксель.

    Private pethods
    ---------------

    - __input_cells()
        Вставляет подготовленные данные в эксель и обновляет страницу для
        пересчета формул.

    - __get_data_from_excel()
        Извлекает указанные ячейки из файла эксель после пересчета формул и
        возвращает их как результат.

    - __copy_cells_to_another_ones()
        Копирует ячейки взятые из ключей словаря self.copy_cells
        во все ячейки, перечисленные в массиве, который является значением

    """

    def __init__(
        self,
        data: dict = {},
        rules: dict | None = None,
        worksheet: str = sett.EMPTY_STRING,
        cells_input: dict | None = None,
        cells_output: dict | None = None,
        copy_cells: dict | None = None,
        additional_input: dict | None = None,
        roundings: dict | None = None,
        settings_file_path: str = sett.SETTINGS_FILE
    ) -> None:
        self.data = data
        self.rules: dict | None = rules
        self.worksheet: str = worksheet
        self.cells_input: dict | None = cells_input
        self.cells_output: dict | None = cells_output
        self.copy_cells: dict[str, list[str]] | None = copy_cells
        self.additional_input: dict[str, Any] | None = additional_input
        self.roundings: dict[str, str] | None = roundings
        self.settings_json_handler: JsonHandler = JsonHandler(
            settings_file_path, True
        )
        self.preparator: DataPreparator = DataPreparator()
        self.excel: win32com.client.CDispatch | None = None
        self.wb: win32com.client.CDispatch | None = None
        self.sheet: win32com.client.CDispatch | None = None
        self.check_err_mesg: str = sett.EMPTY_STRING
        self.settings_file_path: str = settings_file_path

    def initiate_process(self) -> dict:
        """
        Основной метод класса. Запускает процессы проверки и вставки/получения
        данных.

        Returns
        -------
        - data: dict
            Словарь с необработанными данными для вывода в окне результата.
        """

        # Валидация входных данных
        check_result = self.preparator.check_data()
        if not check_result[sett.CHECK_RESULT]:
            return {
                sett.PRICE: None,
                sett.WEIGHT: None,
                sett.ERROR: check_result[sett.ERROR_MESSAGE]
            }

        if not self.__input_cells():
            return {
                sett.PRICE: None,
                sett.WEIGHT: None,
                sett.ERROR: sett.UNKNOWN_ERROR
            }

        if self.copy_cells:
            self.__copy_cells_to_another_ones()

        # Извлечение пересчитанных ячеек
        data = self.__get_data_from_excel()

        return data

    def open_excel(self) -> None:
        """
        Открывает файл для работы и обновляет свойства класса, связанные с
        файлом.
        """

        # Получение пути к файлу эксель, который хранится в файле общих
        # настроек
        file_path = self.settings_json_handler.get_value_by_key(
            sett.EXCEL_PATH
        )

        # Попытка запустить приложение
        try:
            self.excel = win32.DispatchEx(sett.EXCEL_APP)

            # Запуск в фоновом режиме
            self.excel.Visible = sett.EXCEL_VISIBILITY

            # Отключаем предупреждения
            self.excel.DisplayAlerts = sett.EXCEL_DISPLAY_ALERTS

        except Exception as e:
            print(e)

        # Попытка открыть книгу
        try:
            self.wb = self.excel.Workbooks.Open(
                file_path,
                UpdateLinks=sett.EXCEL_UPDATE_LINKS
            )
        except Exception as e:
            print(e)

    def close_excel(self) -> None:
        """
        После работы с файлом, даже когда уже текущее приложение остановлено,
        файл продолжает висеть в задачах и потреблять ресурсы. Этот метод
        принудительно его закрывает.
        """

        # Закрытие книги, если открыта
        if self.sheet:
            self.sheet = None

        if self.wb:
            try:
                self.wb.Close(SaveChanges=sett.EXCEL_SAVE_CHANGES)
                self.wb = None
            except Exception as e:
                print(e)

        # Закрытие приложения эксель, если открыто
        if self.excel:
            try:
                self.excel.Quit()
                self.excel = None
            except Exception as e:
                print(e)

        gc.collect()

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __input_cells(self) -> bool:
        """
        Вызывает процесс подготовки данных и вписывает их в соответствующие
        ячейки в экселе. После чего обновляет страницу, чтобы пересчитались
        формулы.

        Returns
        -------
        - _: bool
            True, если все прошло успешно. False, если произошла ошибка.
        """

        if self.cells_input:
            # Подготавливаем данные для записи в Excel
            self.preparator.data = self.data
            self.preparator.rules = self.rules
            data_prepared = self.preparator.prepare_data(self.cells_input)
            if not data_prepared:
                return False

            # Вставляем данные в Excel
            for cell, value in data_prepared.items():
                self.sheet.Range(cell).Value = value

            # Вставляем доп. данные в Excel
            if self.additional_input:
                for cell, value in self.additional_input.items():
                    self.sheet.Range(cell).Value = value

            # Обновляем связи
            self.wb.RefreshAll()
            self.excel.CalculateUntilAsyncQueriesDone()

        return True

    def __get_data_from_excel(self) -> dict:
        """
        Получаем и округляем цену и вес из таблицы excel.
        При необходимости получаем и другие данные. Это не всегда финишные
        данные. Возможно им будет нужна обработка.

        Returns
        -------
        - excel_data : dict
            Словарь полученными из excel данными.
        """

        # Получение всех необходимых данных
        excel_data = {
            key: self.sheet.Range(self.cells_output[key]).Value
            for key in self.cells_output
        }

        return self.preparator.decimalize_and_rounding(
            excel_data,
            self.roundings
        )

    def __copy_cells_to_another_ones(self) -> None:
        """
        Копирует ячейки взятые из ключей словаря self.copy_cells
        Во все ячейки, перечисленные в массиве, который является значением
        словаря self.copy_cells.
        """

        for cell_to_copy, cells_to_paste_to in self.copy_cells.items():
            cell_to_copy_value = self.sheet.Range(cell_to_copy).Value

            for cell_to_paste_to in cells_to_paste_to:
                self.sheet.Range(cell_to_paste_to).Value = cell_to_copy_value
