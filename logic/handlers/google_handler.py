import os
import requests
import re

from dotenv import load_dotenv

from logic.logger import LogManager as lm
from settings import settings as sett


load_dotenv()
FILE_URL = os.getenv(sett.ENCRYPTION_FILE_LINK)


class GoogleHandler:

    @staticmethod
    def extract_file_id(url) -> str:
        lm.log_method_call()

        match = re.search(sett.GOOGLE_FILE_ID_REGEX, url)
        if match:
            return match.group(1)

        lm.log_error(sett.FILE_ID_PARSING_FALIED)
        raise ValueError(sett.FILE_ID_PARSING_FALIED)

    def get_encryption_file() -> dict:
        lm.log_info(sett.LOG_GET_ENCRYPTION_FILE)
        file_id = GoogleHandler.extract_file_id(FILE_URL)
        download_url = sett.GOOGLE_ENCRYPTION_FILE_LINK.format(file_id)
        response = requests.get(download_url)
        response.raise_for_status()
        return response.json()
