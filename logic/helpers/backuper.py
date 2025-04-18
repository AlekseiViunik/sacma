import os
import shutil

from datetime import datetime, timedelta

from logic.handlers.json_handler import JsonHandler
from logic.logger import LogManager as lm
from logic.protectors.config_protector import ConfigProtector
from settings import settings as sett


class Backuper:
    """
    Класс для создания резервных копий файлов конфигурации приложения.

    Methods
    -------
    - backup_files(settings_path, configs_dir, backup_dir)
        Проверяет дату последнего бэкапа и при необходимости копирует папку
        configs в backups.
    """

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
            lm.log_error(sett.FNF_MESSAGE)
            return

        lm.log_info(sett.TRYING_TO_GET_LAST_BACKUP)
        # Пытаемся получить last_backup datetime из файла настроек
        json_handler = JsonHandler(settings_path, True)
        last_backup = json_handler.get_value_by_key(sett.LAST_BACKUP)
        last_backup_time = datetime.strptime(
            last_backup, sett.DATE_TIME_FORMAT
        ) if last_backup else None
        lm.log_info(sett.LAST_BACKUP_TIME_IS, last_backup_time)

        current_time = datetime.now()

        if (
            not last_backup_time or
            current_time - last_backup_time > timedelta(
                hours=sett.BACKUP_PERIOD
            )
        ):
            lm.log_info(sett.BACKUP_IS_NEEDED)

            if os.path.exists(backup_dir):

                lm.log_info(sett.BACKUP_DIR_EXISTS)
                # Если папка уже существует, то удаляем ее
                try:
                    lm.log_info(sett.TRYING_TO_UNPROTECT_FILES, backup_dir)
                    ConfigProtector.unprotect_all_json_files(backup_dir)

                    lm.log_info(sett.TRYING_TO_DELETE_FILES, backup_dir)
                    shutil.rmtree(backup_dir)

                    lm.log_info(sett.SUCCESS)

                except Exception as e:
                    lm.log_exception(e)

            lm.log_info(sett.CREATE_NEW_NACKUP_FOLDER)
            os.makedirs(backup_dir, exist_ok=True)
            dst = os.path.join(backup_dir, sett.CONFIGS_FOLDER)

            lm.log_info(sett.COPYING_FILES, configs_dir, dst)
            try:
                shutil.copytree(configs_dir, dst)
                lm.log_info(sett.SUCCESS)
            except Exception as e:
                lm.log_exception(e)

            lm.log_info(sett.PROTECTING_FILES, dst)
            ConfigProtector.protect_all_json_files(dst)

            current_time = current_time.strftime(sett.DATE_TIME_FORMAT)
            lm.log_info(sett.REWRITE_LAST_BACKUP_TIME, current_time)
            # Обновляем время бэкапа
            json_handler.write_into_file(
                key=sett.LAST_BACKUP,
                value=current_time
            )
            lm.log_info(sett.BACKUP_SUCCESS)
        else:
            lm.log_info(sett.BACKUP_IS_NOT_NEEDED)
