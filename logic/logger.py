import logging
import os
import sys

from settings import settings as sett

# Путь к файлу логов.
# Если приложение запущено как ехе, то путь будет другой.
if getattr(sys, sett.EXE_FROZEN, False):
    BASE_DIR = os.path.dirname(sys.executable)
    LOG_DIR = os.path.join(BASE_DIR, sett.LOGS_FOLDER_NAME)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(
        BASE_DIR,
        sett.ONE_LEVEL_UP_FOLDER,
        sett.LOGS_FOLDER_NAME
    )

# Создаём папку logs, если её нет.
os.makedirs(LOG_DIR, exist_ok=True)

# Путь к файлу логов.
LOG_FILE = os.path.join(LOG_DIR, sett.LOG_FILE_NAME)


def check_log_size() -> None:
    """
    Проверяет каждый .log файл в папке логов.
    Если количество строк в любом из них превышает лимит — очищает файл.
    """
    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".log"):
            path = os.path.join(LOG_DIR, filename)
            try:
                with open(path, sett.FILE_READ, encoding=sett.STR_CODING) as f:
                    lines = f.readlines()
                if len(lines) >= sett.MAX_LOG_LINES:
                    with open(
                        path, sett.FILE_WRITE, encoding=sett.STR_CODING
                    ) as f:
                        f.write(sett.EMPTY_STRING)
            except Exception as e:
                logger.error(sett.CANT_CLEAR_LOG.format(filename, e))


def switch_log_to_user(username: str) -> None:
    """
    Меняет лог-файл на файл пользователя с именем <username>.log.

    Parameters
    ----------
    - username: str
        Имя пользователя, для которого будет создан лог-файл.
    """
    user_log_file = os.path.join(LOG_DIR, f"{username}.log")

    for h in logger.handlers[:]:
        logger.removeHandler(h)

    user_handler = logging.FileHandler(user_log_file, encoding=sett.STR_CODING)
    user_handler.setFormatter(logging.Formatter(sett.LOGS_FORMAT))

    logger.addHandler(user_handler)


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format=sett.LOGS_FORMAT,  # Формат сообщения
    handlers=[
        logging.FileHandler(LOG_FILE, encoding=sett.STR_CODING),  # Логи в файл
    ]
)

# Создаём логгер
logger = logging.getLogger(sett.APP_LOGGER)
