import os
import requests
import re

from dotenv import load_dotenv

from logic.logger import LogManager as lm
from settings import settings as sett


load_dotenv()
FILE_URL = os.getenv(sett.ENCRYPTION_FILE_LINK)


class GoogleHandler:
    """
    Класс-обработчик для работы с Google Drive API.
    Необходим для получения ключей шифрования из файла, который
    хранится в Google Drive.

    Methods
    -------
    - extract_file_id(url: str) -> str
        Извлекает ID файла из URL Google Drive.

    - get_encryption_file() -> dict
        Получает файл шифрования из Google Drive по ID файла.
        Возвращает его в виде словаря.
    """

    @staticmethod
    def extract_file_id(url) -> str:
        """
        Извлекает ID файла из URL Google Drive.

        Returns
        -------
        - _: str
            ID файла.
        """

        lm.log_method_call()

        match = re.search(sett.GOOGLE_FILE_ID_REGEX, url)
        if match:
            return match.group(1)

        lm.log_error(sett.FILE_ID_PARSING_FALIED)
        raise ValueError(sett.FILE_ID_PARSING_FALIED)

    @staticmethod
    def get_encryption_file() -> dict:
        """
        Получает файл шифрования из Google Drive по ID файла.
        Возвращает его в виде словаря. Словарь содержит ключи шифрования,
        дешифровки и другую информацию, необходимую для дешифровки.
        """

        lm.log_info(sett.TRYING_TO_GET_ENCRYPTION_FILE)
        file_id = GoogleHandler.extract_file_id(FILE_URL)
        download_url = sett.GOOGLE_ENCRYPTION_FILE_LINK.format(file_id)
        response = requests.get(download_url)
        response.raise_for_status()
        return response.json()
