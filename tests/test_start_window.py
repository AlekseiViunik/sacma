from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot

from helpers.finder import Finder
from handlers.json_handler import JsonHandler
from interface.start_window import StartWindow
from settings import settings as sett


config = JsonHandler(sett.MAIN_WINDOW_CONFIG_FILE).get_all_data()[sett.LAYOUT]


def test_start_window_buttons_names(
    start_window: StartWindow,
) -> None:
    """
    Сверяет все наименования кнопок из конфига с созданными кнопками.
    """

    button_names = Finder().find_all_widget_names_by_type(
        config,
        sett.BUTTON,
    )

    actual_buttons = start_window.findChildren(QPushButton)
    actual_button_names = {btn.objectName() for btn in actual_buttons}

    # Переводим список из конфига в множество
    expected_button_names = set(button_names)

    # Сравниваем множества
    assert expected_button_names == actual_button_names, (
        f"Не совпадают кнопки!\n"
        f"Ожидались: {expected_button_names}\n"
        f"Найдены: {actual_button_names}"
    )


def test_widget_amount(
    start_window: StartWindow
):
    """
    Сверяет количество виджетов в конфиге и на окне. Не учитывает контейнеры и
    само окно.
    """

    config_widgets_amout = Finder().find_and_count_all_widgets(config)
    actual_widgets_amount = len(start_window.findChildren(QWidget))
    assert config_widgets_amout == actual_widgets_amount, (
        f"Не совпадает количество виджетов.\n"
        f"Ожидалось: {config_widgets_amout}\n"
        f"Нашлось {actual_widgets_amount}"
    )


def test_open_settings_window(start_window: StartWindow, qtbot: QtBot) -> None:
    """
    Проверяет, что окно настроек открылось и видимо.
    """

    button = start_window.findChild(QPushButton, "Impostazioni")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    assert hasattr(start_window, "settings_window")
    assert start_window.settings_window.isVisible()


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
