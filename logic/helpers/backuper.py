import os
import shutil

from datetime import datetime, timedelta

from logic.handlers.json_handler import JsonHandler
from logic.helpers.helper import Helper
from logic.logger import logger as log
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
            log.warning(
                f"Settings file {settings_path} not found. "
                "Backup will not be created."
            )
            return

        log.info("Get last backup time...")
        # Пытаемся получить last_backup
        json_handler = JsonHandler(settings_path, True)
        last_backup = json_handler.get_value_by_key(sett.LAST_BACKUP)
        last_backup_time = datetime.strptime(
            last_backup, sett.DATE_TIME_FORMAT
        ) if last_backup else None

        log.info("Get current time...")
        current_time = datetime.now()

        log.info("Check if backup is needed...")
        if (
            not last_backup_time or
            current_time - last_backup_time > timedelta(
                hours=sett.BACKUP_PERIOD
            )
        ):
            log.info("It is time to backup!")
            if os.path.exists(backup_dir):
                log.info("Backup folder already exists.")

                log.info("Trying to unprotect all json files...")
                # Если папка уже существует, то удаляем ее
                try:
                    ConfigProtector.unprotect_all_json_files(backup_dir)
                except Exception as e:
                    Helper.log_exception(e)

                log.info("Remove previous backup folder...")
                shutil.rmtree(backup_dir)

            log.info("Create backup folder again...")
            os.makedirs(backup_dir, exist_ok=True)

            log.info("Copy configs folder to backup folder...")
            dst = os.path.join(backup_dir, sett.CONFIGS_FOLDER)
            shutil.copytree(configs_dir, dst)

            log.info("Protect all json files in backup folder...")
            ConfigProtector.protect_all_json_files(dst)

            log.info("Write updated last backup time to settings file...")
            current_time = current_time.strftime(sett.DATE_TIME_FORMAT)
            # Обновляем время бэкапа
            json_handler.write_into_file(
                key=sett.LAST_BACKUP,
                value=current_time
            )
