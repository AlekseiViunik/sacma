import os
import requests
import re

from dotenv import load_dotenv

from settings import settings as sett


load_dotenv()
FILE_URL = os.getenv(sett.ENCRYPTION_FILE_LINK)


class GoogleHandler:

    @staticmethod
    def extract_file_id(url) -> str:
        match = re.search(sett.GOOGLE_FILE_ID_REGEX, url)
        if match:
            return match.group(1)
        raise ValueError(sett.FILE_ID_PARSING_FALIED)

    def get_encryption_file() -> dict:
        file_id = GoogleHandler.extract_file_id(FILE_URL)
        download_url = sett.GOOGLE_ENCRYPTION_FILE_LINK.format(file_id)
        response = requests.get(download_url)
        response.raise_for_status()
        return response.json()
