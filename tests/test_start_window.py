from interface.start_window import StartWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot


def test_open_settings_window(qtbot: QtBot):
    window = StartWindow()
    qtbot.addWidget(window)
    window.show()

    # Ищем кнопку по тексту
    button = window.findChild(QPushButton, "Impostazioni")
    assert button is not None

    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # Проверяем, что settings_window создан и показан
    assert hasattr(window, "settings_window")
    assert window.settings_window.isVisible()
