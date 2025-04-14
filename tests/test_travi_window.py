import pytest

from PyQt6.QtWidgets import QPushButton, QWidget, QComboBox
from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot
from PyQt6.QtTest import QTest

from logic.helpers.finder import Finder
from logic.handlers.json_handler import JsonHandler
from interface.start_window import StartWindow
from settings import settings as sett

config = JsonHandler(sett.TRAVI_WINDOW_CONFIG_FILE).get_all_data()[sett.LAYOUT]


@pytest.fixture
def travi_window(start_window: StartWindow, qtbot: QtBot) -> QWidget:

    # 1. Находим кнопку
    button = start_window.findChild(QPushButton, sett.TRAVI)
    assert button is not None, "Кнопка Travi не найдена"
    assert button.isEnabled(), "Кнопка Travi неактивна"
    assert button.isVisible(), "Кнопка Travi невидима"

    # 2. Активируем окно, на всякий случай
    start_window.raise_()
    start_window.activateWindow()

    # 3. Пробуем кликнуть по кнопке
    try:
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton, delay=10)
    except Exception:
        QTest.mouseClick(button, Qt.MouseButton.LeftButton)

    window = start_window._last_input_window
    assert window.window_name == sett.TRAVI
    return window


def test_travi_sat_widget_count(travi_window: QWidget):
    dropdown = travi_window.findChild(QComboBox, "type")
    assert dropdown is not None, "Комбобокс 'type' не найден"

    dropdown.setCurrentText("SAT")
    config_widgets = Finder().find_all_active_widgets(
        config,
        sett.SAT
    )

    # Дальше можно проверять, сколько виджетов стало
    widgets = travi_window.findChildren(QWidget)
    print(f"Количество виджетов после выбора SAT: {len(widgets)}")
    print(f"Количество виджетов конфига SAT: {len(config_widgets)}")

    # Тут вставишь свою проверку, когда будешь знать, сколько должно быть
    assert len(widgets) > 0
