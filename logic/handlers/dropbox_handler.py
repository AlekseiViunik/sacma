import requests
import os
import tempfile
import psutil
import win32process
import win32com.client as win32

from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.json_handler import JsonHandler
from logic.helpers.helper import Helper
from logic.logger import logger as log
from settings import settings as sett


class DropboxHandler:
    def __init__(
        self,
        excel_handler: ExcelHandler,
        settings_path: str | None = None
    ) -> None:

        self.excel_handler = excel_handler
        self.json_handler = JsonHandler(settings_path, True)

        self.url = None
        self.local_path = os.path.join(
            tempfile.gettempdir(), sett.TEMP_EXCEL_NAME
        )

    def download_excel(self):
        self.url = self.json_handler.get_value_by_key(
            sett.EXCEL_LINK
        ).replace(
            sett.LINK_REPLACE_PART, sett.LINK_REPLACE_WITH
        )
        response = requests.get(self.url)
        response.raise_for_status()
        try:
            with open(self.local_path, sett.FILE_WRITE_BINARY) as file:
                file.write(response.content)
        except PermissionError as pe:
            Helper.log_exception(pe)

    def open_excel(self):

        log.info("Try to close excel if it is already opened...")
        self.__close_excel_if_it_is_already_opened()

        log.info("Try to download excel file...")
        try:
            self.download_excel()
        except Exception as e:
            Helper.log_exception(e)

        self.excel_handler.excel = win32.DispatchEx(sett.EXCEL_APP)

        hwnd = self.excel_handler.excel.Hwnd  # окно Excel
        pid = None

        log.info("Try to get PID of the opened excel...")
        # получаем и сохраняем PID по HWND
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        log.info(f"PID of the opened excel: {pid}. Write it into file...")
        self.json_handler.write_into_file(
            key=sett.LAST_PID,
            value=pid
        )

        self.excel_handler.excel.Visible = sett.EXCEL_VISIBILITY
        self.excel_handler.excel.DisplayAlerts = sett.EXCEL_DISPLAY_ALERTS
        self.excel_handler.wb = self.excel_handler.excel.Workbooks.Open(
            self.local_path, UpdateLinks=sett.EXCEL_UPDATE_LINKS
        )

    def close_excel(self):
        log.info("Try to close and remove excel...")
        self.excel_handler.close_excel()
        if os.path.exists(self.local_path):
            try:
                os.remove(self.local_path)
                log.info("Excel file removed successfully.")
            except PermissionError:
                log.info(
                    "Excel file is opened. Try to remove it after closing."
                )
                self.__close_excel_if_it_is_already_opened()
                try:
                    os.remove(self.local_path)
                    log.info("Excel file removed successfully.")
                except PermissionError as pe:
                    Helper.log_exception(pe)
            except Exception as e:
                Helper.log_exception(e)

    def restart_excel(self, user_settings_path: str):
        """
        Закрывает текущий экземпляр Excel и скачивает и открывает новый
        учитывая, что файл с содержанием пути к файлу excel мог измениться
        или вообще стать другим.

        Parameters
        ----------
        - new_settings_filepath: str
            Новый путь к файлу настроек, в котором хранится ссылка на эксель.
        """
        log.info("Restart excel...")
        self.close_excel()

        log.info("Set new settings path...")
        self.json_handler.set_file_path(user_settings_path)
        self.json_handler.create_file_if_not_exists()
        if not sett.TEST_GUI:
            log.info("Try to reopen excel...")
            self.open_excel()

    def __close_excel_if_it_is_already_opened(self) -> None:
        """
        Проверяет, открыт ли Excel. Если открыт, то закрывает, иначе
        ничего не делает. Проверка осуществляется по PID, который
        сохраняется в файле настроек. Если PID не найден, значит
        Excel не открыт.
        """

        last_pid = self.json_handler.get_value_by_key(
            sett.LAST_PID
        )

        if last_pid and psutil.pid_exists(last_pid):

            log.info("Try to stop excel process...")
            try:
                proc = psutil.Process(last_pid)
                proc.terminate()
            except Exception as e:
                Helper.log_exception(e)
