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


def check_log_size() -> None:
    """
    Метод проверяет текущий размер файла логирования перед стартом приложения.
    Если количество строк в файле превышает заданное, то файл очищается и
    начинает писаться заново.
    """
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding=set.LOG_CODING) as f:
            lines = f.readlines()

        if len(lines) >= set.MAX_LOG_LINES:
            with open(LOG_FILE, "w", encoding=set.LOG_CODING) as f:
                f.write("")  # Очищаем файл


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",  # Формат сообщения
    handlers=[
        logging.FileHandler(LOG_FILE, encoding=set.LOG_CODING),  # Логи в файл
    ]
)

# Создаём логгер
logger = logging.getLogger("AppLogger")
