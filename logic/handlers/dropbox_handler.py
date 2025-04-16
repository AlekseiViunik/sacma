import requests
import os
import tempfile
import psutil
import win32process
import win32com.client as win32

from logic.handlers.excel_handler import ExcelHandler
from logic.handlers.json_handler import JsonHandler
from logic.helpers.helper import Helper
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
        self.__close_excel_if_it_is_already_opened()
        self.download_excel()
        self.excel_handler.excel = win32.DispatchEx(sett.EXCEL_APP)

        hwnd = self.excel_handler.excel.Hwnd  # окно Excel
        pid = None

        # получаем и сохраняем PID по HWND
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
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
        self.excel_handler.close_excel()
        if os.path.exists(self.local_path):
            try:
                os.remove(self.local_path)
            except PermissionError:
                self.__close_excel_if_it_is_already_opened()

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

        self.close_excel()
        self.json_handler.set_file_path(user_settings_path)
        self.json_handler.create_file_if_not_exists()
        if not sett.TEST_GUI:
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
            try:
                proc = psutil.Process(last_pid)
                proc.terminate()
            except Exception as e:
                Helper.log_exception(e)
