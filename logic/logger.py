import logging
import os

from settings import settings as set

# Путь к файлу логов
LOG_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "logs"
)
os.makedirs(LOG_DIR, exist_ok=True)  # Создаём папку logs, если её нет
LOG_FILE = os.path.join(LOG_DIR, set.LOG_FILE_NAME)


def check_log_size():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) >= set.MAX_LOG_LINES:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write("")  # Очищаем файл


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",  # Формат сообщения
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # Логи в файл
    ]
)

# Создаём логгер
logger = logging.getLogger("AppLogger")
