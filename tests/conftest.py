import pytest
from PyQt6.QtWidgets import QApplication
import sys

from pathlib import Path

# Добавляем корень проекта в sys.path. Нужно для правильного использования
# импортов основного приложения.
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))


@pytest.fixture(scope="session")
def app():
    return QApplication(sys.argv)
