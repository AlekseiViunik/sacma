import logging
import os
import sys
import traceback
import inspect

from logic.generators.filepath_generator import FilepathGenerator as FP
from settings import settings as sett

_logger_instance = None


class ContextLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        # Пробегаем стек до первого вызова вне логгера
        frame = inspect.currentframe()
        while frame:
            code = frame.f_code.co_name
            if code not in (
                "info", "error", "log_info", "log_error", "log_exception",
                "process", "log"
            ):
                break
            frame = frame.f_back

        func_name = frame.f_code.co_name if frame else "?"
        cls_name = type(
            frame.f_locals.get("self", object())
        ).__name__ if frame else "?"
        context = (
            f"{cls_name}.{func_name}" if cls_name != "object" else func_name
        )

        kwargs["extra"] = kwargs.get("extra", {})
        kwargs["extra"]["context"] = context
        return msg, kwargs


class ContextFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "context"):
            record.context = "-"
        return super().format(record)


class LogManager:
    """
    Кастомный логгер для приложения.
    Пишет логи в формате Дата и время| Тип | Имя класса.Имя метода | Сообщение.

    Methods
    -------
    - setup_default_logger()
        Настройка логгера по умолчанию. Создает папку для логов, если она не
        существует, и создает файл лога с именем "app.log".

    - switch_log_to_user(username: str) -> None
        Переключает логирование на пользователя с указанным именем. Создает
        (если надо) файл лога с именем "username.log" в папке логов. Удаляет
        старый обработчик и добавляет новый. который пишет логи уже в только
        что созданную папку.

    - get_log_dir() -> str
        Возвращает путь к папке с логами в зависимости от того, запущено
        приложение из exe или из py.

    - log_info(message, *args) -> None
        Записывает информационное сообщение в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

    - log_error(message, *args) -> None
        Записывает сообщение об ошибке в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

    - log_warning(message, *args) -> None
        Записывает предупреждение в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

    - log_critical(message, *args) -> None
        Записывает критическую ошибку в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

    - log_exception(e: Exception) -> None
        Записывает информацию об исключении в лог.

    - log_method_call() -> None
        Записывает информацию о вызове метода в лог.

    - check_log_size() -> None
        Проверяет размер логов в папке с логами. Если размер превышает
        MAX_LOG_LINES, очищает лог.
    """

    @staticmethod
    def setup_default_logger() -> None:
        """
        Настройка логгера по умолчанию. Создает папку для логов, если она не
        существует, и создает файл лога с именем "app.log".
        Использует кастомный адаптер и форматтер для того, чтобы добавить
        Класс.методо, из которого был записан конкретный лог.
        """

        global _logger_instance

        if getattr(sys, sett.EXE_FROZEN, False):
            base_dir = os.path.dirname(sys.executable)
            log_dir = os.path.join(base_dir, sett.LOGS_FOLDER_NAME)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_dir = os.path.join(
                base_dir,
                sett.ONE_LEVEL_UP_FOLDER,
                sett.LOGS_FOLDER_NAME
            )

        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, sett.LOG_FILE_NAME)

        handler = logging.FileHandler(log_file, encoding=sett.STR_CODING)
        handler.setFormatter(ContextFormatter(sett.LOGS_FORMAT))

        logger = logging.getLogger(sett.APP_LOGGER)
        logger.handlers.clear()  # Очистить все обработчики
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        _logger_instance = ContextLoggerAdapter(logger, {})

    @staticmethod
    def switch_log_to_user(username: str) -> None:
        """
        Переносит логирование в другую папку каждый раз когда меняется
        пользователь.

        Parameters
        ----------
        - username: str
            Имя пользователя, для которого будет создан/использован лог.
        """

        global _logger_instance

        user_log_file = FP.generate_log_filepath(
            LogManager.get_log_dir(), username
        )

        logger = logging.getLogger(sett.APP_LOGGER)
        logger.handlers.clear()  # Очистить все обработчики

        user_handler = logging.FileHandler(
            user_log_file,
            encoding=sett.STR_CODING
        )
        user_handler.setFormatter(ContextFormatter(sett.LOGS_FORMAT))
        logger.addHandler(user_handler)
        logger.setLevel(logging.INFO)

        _logger_instance = ContextLoggerAdapter(logger, {})

    @staticmethod
    def get_log_dir() -> str:
        """
        Возвращает относительный или абсолютный путь к папке с логами в
        зависимости от того, запущено приложение из exe или из py.

        Returns
        -------
        - _: str
            Путь к папке с логами.
        """

        if getattr(sys, sett.EXE_FROZEN, False):
            return os.path.join(
                os.path.dirname(sys.executable),
                sett.LOGS_FOLDER_NAME
            )
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            sett.ONE_LEVEL_UP_FOLDER,
            sett.LOGS_FOLDER_NAME
        )

    @staticmethod
    def log_info(message: str, *args) -> None:
        """
        Записывает информационное сообщение в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

        Parameters
        ----------
        - message: str
            Сообщение для записи в лог.

        - args: tuple
            Аргументы для форматирования сообщения.
        """

        if args:
            message = message.format(*args)
        _logger_instance.info(message)

    @staticmethod
    def log_error(message: str, *args) -> None:
        """
        Записывает сообщение об ошибке в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

        Parameters
        ----------
        - message: str
            Сообщение для записи в лог.

        - args: tuple
            Аргументы для форматирования сообщения.
        """

        if args:
            message = message.format(*args)
        _logger_instance.error(message)

    @staticmethod
    def log_warning(message: str, *args) -> None:
        """
        Записывает предупреждение в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

        Parameters
        ----------
        - message: str
            Сообщение для записи в лог.

        - args: tuple
            Аргументы для форматирования сообщения.
        """

        if args:
            message = message.format(*args)
        _logger_instance.warning(message)

    @staticmethod
    def log_critical(message: str, *args) -> None:
        """
        Записывает критическую ошибку в лог. Если переданы аргументы,
        форматирует сообщение с их помощью.

        Parameters
        ----------
        - message: str
            Сообщение для записи в лог.

        - args: tuple
            Аргументы для форматирования сообщения.
        """

        if args:
            message = message.format(*args)
        _logger_instance.critical(message)

    @staticmethod
    def log_exception(e: Exception) -> None:
        """
        Записывает информацию об исключении в лог.
        Использует traceback для получения информации о месте возникновения
        исключения.

        Parameters
        ----------
        - e: Exception
            Исключение, которое нужно записать в лог.
        """

        exc_info = traceback.extract_tb(e.__traceback__)[-1]
        filename = exc_info.filename
        line = exc_info.lineno
        func = exc_info.name
        full_msg = sett.EXCEPTION_MSG_TEMPLATE.format(
            type(e).__name__, e, func, filename, line
        )
        _logger_instance.critical(sett.ERROR_CAUGHT.format(full_msg))

    @staticmethod
    def log_method_call():
        """
        Записывает информацию о вызове метода в лог.
        """

        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        cls_name = type(frame.f_locals.get("self", object())).__name__
        context = (
            f"{cls_name}.{func_name}" if cls_name != "object" else func_name
        )
        LogManager.log_info("Method {0} called.", context)

    @staticmethod
    def check_log_size() -> None:
        """
        Проверяет все логи в папке с логами. Если размер лога превышает
        MAX_LOG_LINES (20 000 по умолчанию), очищает лог.
        """

        for filename in os.listdir(LogManager.get_log_dir()):
            if filename.endswith(sett.LOG_EXTENSION):
                path = os.path.join(LogManager.get_log_dir(), filename)
                try:
                    with open(
                        path,
                        sett.FILE_READ,
                        encoding=sett.STR_CODING
                    ) as f:
                        lines = f.readlines()
                    if len(lines) >= sett.MAX_LOG_LINES:
                        with open(
                            path,
                            sett.FILE_WRITE,
                            encoding=sett.STR_CODING
                        ) as f:
                            f.write(sett.EMPTY_STRING)
                except Exception as e:
                    LogManager.log_error(sett.CANT_CLEAR_LOG, filename, e)
