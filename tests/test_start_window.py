from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot

from handlers.json_handler import JsonHandler
from interface.start_window import StartWindow
from interface.windows.settings_window import SettingsWindow
from settings import settings as sett


config = JsonHandler(sett.MAIN_WINDOW_CONFIG_FILE).get_all_data()[sett.LAYOUT]


class FakeExcelHandler:
    def open_excel(self): pass
    def close_excel(self): pass
    def restart_excel(self, *args): pass


def fake_exec(self):
    self.show()
    return 1  # имитируем "Accepted"


def test_open_settings_window(
    start_window: StartWindow,
    qtbot: QtBot,
    monkeypatch
) -> None:

    start_window.excel_handler = FakeExcelHandler()
    monkeypatch.setattr(SettingsWindow, "exec", fake_exec)

    button = start_window.findChild(QPushButton, "Impostazioni")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "settings_window")


def test_open_create_user_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно настроек открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Create user")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "register_window")
    assert start_window.register_window.isVisible()


def test_open_travi_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Travi открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Travi")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_fiancate_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Fiancate открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Fiancate")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_tasselli_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Tasselli не открылось и не видимо.
    """

    button = start_window.findChild(QPushButton, "Tasselli")
    assert button is not None
    assert not button.isEnabled(), "Кнопка Tasselli должна быть неактивна"

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # Проверяем, что атрибут не появился
    assert not hasattr(start_window, "_last_input_window"), (
        "Окно ввода не должно было быть открыто"
    )


def test_open_satellitare_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Satellitare открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Satellitare")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_pianetti_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Pianetti открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Pianetti")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_grigliato_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Grigliato открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Grigliato")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_travi_di_battuta_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Travi di battuta открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Travi di battuta")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_angolari_per_automatici_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Angolari per automatici открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Angolari per automatici")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()


def test_open_gravita_leggera_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Gravità leggera не открылось и не видимо.
    """

    button = start_window.findChild(QPushButton, "Gravità leggera")
    assert button is not None
    assert not button.isEnabled(), (
        "Кнопка Gravità leggera должна быть неактивна"
    )

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # Проверяем, что атрибут не появился
    assert not hasattr(start_window, "_last_input_window"), (
        "Окно ввода не должно было быть открыто"
    )


def test_open_option_di_sicurezza_window(
    start_window: StartWindow,
    qtbot: QtBot
) -> None:
    """
    Проверяет, что окно Option di sicurezza открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Option di sicurezza")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "_last_input_window")
    assert start_window._last_input_window.isVisible()
    assert start_window._last_input_window.window_name == "Option di sicurezza"
