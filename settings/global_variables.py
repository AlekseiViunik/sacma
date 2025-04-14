from settings import settings as sett
from logic.handlers.google_handler import GoogleHandler

global encryption_data

if sett.PRODUCTION_MODE_ON:
    # Получаем данные шифрования из Google Drive
    encryption_data = GoogleHandler.get_encryption_file()
else:
    encryption_data = {}
