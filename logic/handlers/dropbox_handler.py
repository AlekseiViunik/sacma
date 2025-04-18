import os
import psutil
import requests

import win32process
import win32com.client as win32

from logic.generators.filepath_generator import FilepathGenerator as FP
from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.json_handler import JsonHandler
from logic.logger import LogManager as lm
from settings import settings as sett


class DropboxHandler:
    """
    Обработчик для работы с Excel файлами, которые хранятся в Dropbox.
    Скачивает файл по ссылке, открывает его в Excel и сохраняет PID
    процесса Excel в JSON файл. Также закрывает Excel и удаляет файл
    после завершения работы.

    Attributes
    ----------
    - excel_handler: ExcelHandler
        Обработчик для работы с Excel файлами.

    - settings_path: str | None
        Путь к файлу настроек, в котором хранится ссылка на файл
        Excel в Dropbox, а также PID последнего запущенного процесса.

    Methods
    -------
    - download_excel()
        Скачивает файл Excel из Dropbox по ссылке, указанной в
        файле настроек. Сохраняет файл во временной директории.

    - open_excel()
        Открывает файл Excel в приложении Excel. Если файл уже
        открыт, закрывает его и открывает заново.

    - close_excel()
        Закрывает приложение Excel и удаляет временный файл
        Excel из локальной директории.

    - restart_excel(user_settings_path: str)
        Закрывает текущий экземпляр Excel и скачивает и открывает новый
        учитывая, что файл с содержанием пути к файлу excel мог измениться
        или вообще стать другим.

    Private Methods
    ---------------
    - __close_excel_if_it_is_already_opened()
        Закрывает приложение Excel, если оно уже открыто. Проверяет
        по PID, сохраненному в файле настроек. Если PID не найден,
        значит Excel не открыт.
    """

    def __init__(
        self,
        excel_handler: ExcelHandler,
        settings_path: str | None = None
    ) -> None:

        self.excel_handler = excel_handler
        self.json_handler = JsonHandler(settings_path, True)

        self.url = None
        self.local_path = FP.generate_temp_excel_filepath()

    def download_excel(self) -> None:
        """
        Скачивает файл Excel из Dropbox по ссылке, указанной в
        файле настроек. Сохраняет файл во временной директории.
        """

        lm.log_method_call()

        lm.log_info(sett.GETTING_EXCEL_LINK)
        self.url = self.json_handler.get_value_by_key(
            sett.EXCEL_LINK
        ).replace(
            sett.LINK_REPLACE_PART, sett.LINK_REPLACE_WITH
        )
        lm.log_info(sett.EXCEL_LINK_IS, self.url)

        lm.log_info(sett.DOWNLOAD_FILE_FROM_DROPBOX)
        response = requests.get(self.url)
        response.raise_for_status()

        lm.log_info(sett.TRYING_TO_OPEN_DOWNLOADED_FILE)
        try:
            with open(self.local_path, sett.FILE_WRITE_BINARY) as file:
                file.write(response.content)
            lm.log_info(sett.SUCCESS)
        except PermissionError as pe:
            lm.log_exception(pe)

    def open_excel(self) -> None:
        """
        Открывает скачанный во временную директорию файл Excel, предварительно
        попытавшись закрыть открытые в предыдущей сессии файлы, устанавливает
        свойства обработчика эксель. Записывает PID процесса Excel в файл
        настроек.
        """

        lm.log_method_call()
        lm.log_info(sett.TRYING_TO_CLOSE_EXCEL)
        self.__close_excel_if_it_is_already_opened()

        lm.log_info(sett.TRYING_TO_DOWNLOAD_EXCEL)
        try:
            self.download_excel()
            lm.log_info(sett.SUCCESS)
        except Exception as e:
            lm.log_exception(e)

        lm.log_info(sett.TRYING_TO_OPEN_EXCEL_APP)
        try:
            self.excel_handler.excel = win32.DispatchEx(sett.EXCEL_APP)
            lm.log_info(sett.SUCCESS)
        except Exception as e:
            lm.log_exception(e)

        lm.log_info(sett.GETTING_PID)
        hwnd = self.excel_handler.excel.Hwnd  # окно Excel
        pid = None
        # получаем и сохраняем PID по HWND
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        lm.log_info(sett.SAVE_PID, pid)
        self.json_handler.write_into_file(
            key=sett.LAST_PID,
            value=pid
        )

        lm.log_info(sett.SET_EXCEL_SETTINGS)
        self.excel_handler.excel.Visible = sett.EXCEL_VISIBILITY
        self.excel_handler.excel.DisplayAlerts = sett.EXCEL_DISPLAY_ALERTS

        lm.log_info(sett.TRYING_TO_OPEN_EXCEL_WB)
        try:
            self.excel_handler.wb = self.excel_handler.excel.Workbooks.Open(
                self.local_path, UpdateLinks=sett.EXCEL_UPDATE_LINKS
            )
            lm.log_info(sett.SUCCESS)
        except Exception as e:
            lm.log_exception(e)

    def close_excel(self) -> None:
        """
        Закрывает приложение Excel используя обработчик ExcelHandler.
        Удаляет временный файл Excel из локальной директории. Если по какой-то
        причине файл закрыть или удалить не удалось, использует убийцу
        процессов.
        """

        lm.log_method_call()
        lm.log_info(sett.CLOSE_EXCEL_HANDLER_FIRST)
        self.excel_handler.close_excel()

        if os.path.exists(self.local_path):
            lm.log_info(sett.TRYING_TO_DELETE_EXCEL_FILE)
            try:
                os.remove(self.local_path)
                lm.log_info(sett.SUCCESS)
            except PermissionError:
                lm.log_error(sett.CANT_DELETE_EXCEL_FILE)
                self.__close_excel_if_it_is_already_opened()
                lm.log_info(sett.TRYING_TO_DELETE_EXCEL_FILE_2)
                try:
                    os.remove(self.local_path)
                    lm.log_info(sett.SUCCESS)
                except PermissionError as pe:
                    lm.log_exception(pe)
            except Exception as e:
                lm.log_exception(e)

    def restart_excel(self, user_settings_path: str):
        """
        Закрывает текущий экземпляр Excel и скачивает и открывает новый
        учитывая, что файл с содержанием пути к файлу excel мог измениться
        или вообще стать другим.

        Parameters
        ----------
        - user_settings_path: str
            Новый путь к файлу настроек, в котором хранится ссылка на эксель.
        """

        lm.log_method_call()
        lm.log_info(sett.RESTART_EXCEL)
        self.close_excel()

        lm.log_info(sett.SET_NEW_FILEPATH)
        self.json_handler.set_file_path(user_settings_path)

        lm.log_info(sett.CREATE_SETTINGS_FILE_IF_NOT_EXISTS)
        self.json_handler.create_file_if_not_exists()

        if not sett.TEST_GUI:
            lm.log_info(sett.TRYING_TO_OPEN_EXCEL_AGAIN)
            self.open_excel()

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __close_excel_if_it_is_already_opened(self) -> None:
        """
        Проверяет, открыт ли Excel. Если открыт, то закрывает, иначе
        ничего не делает. Проверка осуществляется по PID, который
        сохраняется в файле настроек. Если PID не найден, значит
        Excel не открыт. Если PID найден, то проверяет, существует ли
        процесс с таким PID. Если существует, то убивает его.
        """

        lm.log_method_call()

        lm.log_info(sett.GET_LAST_PID)
        last_pid = self.json_handler.get_value_by_key(
            sett.LAST_PID
        )

        if last_pid and psutil.pid_exists(last_pid):
            lm.log_info(sett.PID_AND_PROCESS_FOUND, last_pid)

            lm.log_info(sett.TRYING_TO_KILL_PROCESS, last_pid)
            try:
                proc = psutil.Process(last_pid)
                proc.terminate()
                lm.log_info(sett.SUCCESS)
            except Exception as e:
                lm.log_exception(e)
