# noinspection PyUnresolvedReferences
import tests.conftest_imports  # noqa: F401

import logging
import pytest

from PyQt6.QtWidgets import QApplication

from handlers.excel_handler import ExcelHandler
from interface.start_window import StartWindow


@pytest.fixture(scope="session")
def app():
    return QApplication([])


@pytest.fixture
def start_window(qtbot):
    window = StartWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@pytest.fixture(autouse=True, scope="session")
def disable_logging():
    logging.disable(logging.CRITICAL)


@pytest.fixture(scope="session")
def excel_handler():
    handler = ExcelHandler()
    handler.open_excel()  # Открываем один раз
    yield handler
    handler.close_excel()
