from settings import settings as sett


class FilepathGenerator:
    """
    Генератор путей для файлов настроек и конфигураций.

    Methods
    -------
    - generate_config_filepath(path, username)
        Генерирует путь к файлу конфигурации для указанного пользователя.
    """

    @staticmethod
    def generate_settings_filepath(path: str, username: str) -> str:
        return path.replace(
            sett.SETTINGS_JSON,
            sett.MODIFIED_SETTINGS_JSON.format(username)
        )
