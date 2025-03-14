from PyQt6.QtWidgets import QApplication, QWidget


class Helper:

    @staticmethod
    def move_window_to_center(window: QWidget):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - window.window_width) // 2
        y = (screen_geometry.height() - window.window_height) // 2
        window.setGeometry(x, y, window.window_width, window.window_height)

    @staticmethod
    def move_window_to_top_left_corner(window: QWidget):
        window.setGeometry(0, 0, window.window_width, window.window_height)
