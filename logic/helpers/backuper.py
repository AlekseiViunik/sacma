import os
import shutil

from datetime import datetime, timedelta

from logic.handlers.json_handler import JsonHandler
from logic.protectors.config_protector import ConfigProtector
from settings import settings as sett


class Backuper:

    @staticmethod
    def backup_files(
        settings_path: str,
        configs_dir: str,
        backup_dir: str
    ) -> None:
        """
        Проверяет дату последнего бэкапа и при необходимости копирует папку
        configs в backups.

        Parameters
        ----------
        - settings_path: str
            Путь к файлу настроек приложения, в котором указана дата
            последнего бэкапа.
        - configs_dir: str
            Путь к папке, которую нужно бэкапить.
        - backup_dir: str
            Путь к папке, куда будет сохранен бэкап.
        """

        if not os.path.exists(settings_path):
            return

        # Пытаемся получить last_backup
        json_handler = JsonHandler(settings_path, True)
        last_backup = json_handler.get_value_by_key(sett.LAST_BACKUP)
        last_backup_time = datetime.strptime(
            last_backup, sett.DATE_TIME_FORMAT
        ) if last_backup else None
        current_time = datetime.now()
        if (
            not last_backup_time or
            current_time - last_backup_time > timedelta(
                hours=sett.BACKUP_PERIOD
            )
        ):
            if os.path.exists(backup_dir):
                ConfigProtector.unprotect_all_json_files(backup_dir)
                shutil.rmtree(backup_dir)
            os.makedirs(backup_dir, exist_ok=True)

            dst = os.path.join(backup_dir, sett.CONFIGS_FOLDER)
            shutil.copytree(configs_dir, dst)
            ConfigProtector.protect_all_json_files(dst)

            current_time = current_time.strftime(sett.DATE_TIME_FORMAT)
            # Обновляем время бэкапа
            json_handler.write_into_file(
                key=sett.LAST_BACKUP,
                value=current_time
            )
