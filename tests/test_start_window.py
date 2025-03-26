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
    print(f"Widgets in config: {config_widgets_amout}")
    print(f"Widgets on window: {actual_widgets_amount}")
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
