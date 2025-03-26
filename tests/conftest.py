import pytest
import sys

from pathlib import Path
from PyQt6.QtWidgets import QApplication

from interface.start_window import StartWindow


# Добавляем корень проекта в sys.path. Нужно для правильного использования
# импортов основного приложения.
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))


@pytest.fixture(scope="session")
def app():
    return QApplication(sys.argv)


@pytest.fixture
def start_window(qtbot):
    window = StartWindow()
    qtbot.addWidget(window)
    window.show()
    return window
