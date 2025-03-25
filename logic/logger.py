import logging
import os
import sys

from settings import settings as set

# Путь к файлу логов.
# Если приложение запущено как ехе, то путь будет другой.
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    LOG_DIR = os.path.join(BASE_DIR, set.LOGS_FOLDER_NAME)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(
        BASE_DIR,
        set.ONE_LEVEL_UP_FOLDER,
        set.LOGS_FOLDER_NAME
    )

# Создаём папку logs, если её нет.
os.makedirs(LOG_DIR, exist_ok=True)

# Путь к файлу логов.
LOG_FILE = os.path.join(LOG_DIR, set.LOG_FILE_NAME)


def check_log_size() -> None:
    """
    Метод проверяет текущий размер файла логирования перед стартом приложения.
    Если количество строк в файле превышает заданное, то файл очищается и
    начинает писаться заново.
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, set.FILE_READ, encoding=set.STR_CODING) as f:
            lines = f.readlines()

        if len(lines) >= set.MAX_LOG_LINES:
            with open(LOG_FILE, set.FILE_WRITE, encoding=set.STR_CODING) as f:
                f.write(set.EMPTY_STRING)  # Очищаем файл


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",  # Формат сообщения
    handlers=[
        logging.FileHandler(LOG_FILE, encoding=set.STR_CODING),  # Логи в файл
    ]
)

# Создаём логгер
logger = logging.getLogger(set.APP_LOGGER)
