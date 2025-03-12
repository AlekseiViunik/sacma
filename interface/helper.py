from PyQt6.QtWidgets import QApplication, QWidget


class Helper:

    @staticmethod
    def move_window_to_center(window: QWidget):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - window.width) // 2
        y = (screen_geometry.height() - window.height) // 2
        window.setGeometry(x, y, window.width, window.height)
