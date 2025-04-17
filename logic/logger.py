import inspect
import logging
import os
import sys
import traceback

from settings import settings as sett


class LogManager:
    logger = logging.getLogger(sett.APP_LOGGER)

    @staticmethod
    def setup_default_logger():
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

        logging.basicConfig(
            level=logging.INFO,
            format=sett.LOGS_FORMAT,
            handlers=[
                logging.FileHandler(log_file, encoding=sett.STR_CODING),
            ]
        )

    @staticmethod
    def switch_log_to_user(username: str) -> None:
        user_log_file = os.path.join(
            LogManager.get_log_dir(), f"{username}.log"
        )

        for h in LogManager.logger.handlers[:]:
            LogManager.logger.removeHandler(h)

        user_handler = logging.FileHandler(
            user_log_file, encoding=sett.STR_CODING
        )
        user_handler.setFormatter(logging.Formatter(sett.LOGS_FORMAT))
        LogManager.logger.addHandler(user_handler)

    @staticmethod
    def get_log_dir() -> str:
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
        if args:
            message = message.format(*args)
        LogManager.logger.info(message)

    @staticmethod
    def log_error(message: str, *args) -> None:
        if args:
            message = message.format(*args)
        LogManager.logger.error(message)

    @staticmethod
    def log_exception(e: Exception) -> None:
        exc_info = traceback.extract_tb(e.__traceback__)[-1]
        filename = exc_info.filename
        line = exc_info.lineno
        func = exc_info.name
        full_msg = sett.EXCEPTION_MSG_TEMPLATE.format(
            type(e).__name__, e, func, filename, line
        )
        LogManager.logger.error(sett.ERROR_CAUGHT.format(full_msg))

    @staticmethod
    def log_method_call():
        context = LogManager._get_caller_context()
        LogManager.log_info("Method {0} called.", context)

    @staticmethod
    def check_log_size() -> None:
        for filename in os.listdir(LogManager.get_log_dir()):
            if filename.endswith(".log"):
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

    @staticmethod
    def _get_caller_context() -> str:
        frame = inspect.currentframe()
        outer = frame.f_back.f_back
        func_name = outer.f_code.co_name
        cls_name = type(outer.f_locals.get("self", object())).__name__
        return f"{cls_name}.{func_name}" if cls_name != "object" else func_name
