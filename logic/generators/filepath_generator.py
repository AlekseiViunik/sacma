import os
import tempfile

from settings import settings as sett


class FilepathGenerator:
    """
    Генератор путей для файлов настроек и конфигураций.

    Methods
    -------
    - generate_settings_filepath(path, username)
        Генерирует путь к файлу конфигурации для указанного пользователя.

    - generate_log_filepath(path, username)
        Генерирует путь к файлу журнала логов для указанного пользователя.

    - generate_temp_excel_filepath()
        Генерирует путь к временной директории для Excel файла.
    """

    @staticmethod
    def generate_settings_filepath(path: str, username: str) -> str:
        """
        Генерирует путь к файлу настроек для указанного пользователя.

        Parameters
        ----------
        - path: str
            Путь к файлу настроек.

        - username: str
            Имя пользователя, для которого генерируется путь.

        Returns
        -------
        - _: str
            Путь к файлу настроек для указанного пользователя.
        """

        return path.replace(
            sett.SETTINGS_JSON,
            sett.MODIFIED_SETTINGS_JSON.format(username)
        )

    @staticmethod
    def generate_log_filepath(path: str, username: str) -> str:
        """
        Генерирует путь к файлу журнала логов для указанного пользователя.

        Parameters
        ----------
        - path: str
            Путь к папке с логами.

        - username: str
            Имя пользователя, для которого генерируется путь.

        Returns
        -------
        - _: str
            Путь к файлу журнала логов для указанного пользователя.
        """

        return os.path.join(path, sett.MODIFIED_LOG_PATH.format(username))

    @staticmethod
    def generate_temp_excel_filepath() -> str:
        """
        Генерирует путь к временной директории для Excel файла. Для
        генерации используется временная директория операционной
        системы.

        Returns
        -------
        - _: str
            Путь к временной директории для Excel файла.
        """

        return os.path.join(tempfile.gettempdir(), sett.TEMP_EXCEL_NAME)
