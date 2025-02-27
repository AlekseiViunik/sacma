import logging
import os

# Путь к файлу логов
LOG_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "logs"
)
os.makedirs(LOG_DIR, exist_ok=True)  # Создаём папку logs, если её нет
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",  # Формат сообщения
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # Логи в файл
        logging.StreamHandler()  # Логи в консоль
    ]
)

# Создаём логгер
logger = logging.getLogger("AppLogger")
