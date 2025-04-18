from PyQt6.QtWidgets import QApplication, QWidget

from settings import settings as sett


class Mover:
    """
    Класс, который отвечает за перемещение окон в разные позиции на экране.
    В основном используется для перемещения окон в центр экрана.

    Methods
    -------
    - move_window_to_center(window: QWidget) -> None
        Сдвигает в центр указанное окно.

    - move_window_to_top_left_corner(window: QWidget) -> None
        Сдвигает в верхний левый угол указанное окно.

    - move_window_to_top_center(window: QWidget) -> None
        Сдвигает в верхний центр указанное окно.
    """

    @staticmethod
    def move_window_to_center(window: QWidget) -> None:
        """
        Сдвигает в центр указанное окно.

        Parameters
        ----------
        - window: QWidget
            Окно, которое нужно сдвинуть.
        """

        screen_geometry = QApplication.primaryScreen().geometry()

        x = (
            screen_geometry.width() - window.window_width
        ) // sett.MIDDLE_DETERMINANT_DIVIDER

        y = (
            screen_geometry.height() - window.window_height
        ) // sett.MIDDLE_DETERMINANT_DIVIDER

        window.setGeometry(x, y, window.window_width, window.window_height)

    @staticmethod
    def move_window_to_top_left_corner(window: QWidget) -> None:
        """
        Сдвигает в верхний левый угол указанное окно.

        Parameters
        ----------
        - window: QWidget
            Окно, которое нужно сдвинуть.
        """

        window.setGeometry(
            sett.TOP_LEFT_X,
            sett.TOP_Y,
            window.window_width,
            window.window_height
        )

    @staticmethod
    def move_window_to_top_center(window: QWidget) -> None:
        """
        Сдвигает в верхний центр указанное окно.

        Parameters
        ----------
        - window: QWidget
            Окно, которое нужно сдвинуть.
        """

        screen_geometry = QApplication.primaryScreen().geometry()

        x = (
            screen_geometry.width() - window.window_width
        ) // sett.MIDDLE_DETERMINANT_DIVIDER

        y = sett.TOP_Y

        window.setGeometry(x, y, window.window_width, window.window_height)
