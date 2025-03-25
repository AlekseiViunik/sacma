from PyQt6.QtWidgets import QMessageBox, QWidget

from settings import settings as set


class Messagebox:

    @staticmethod
    def show_messagebox(
        title: str,
        msg: str,
        window: QWidget,
        type: str = set.ERROR
    ) -> None:
        """
        Выводит окно об ошибке или просто информационное окно (разница только в
        иконке) в зависимости от указанного type. Окно выводится относительно
        окна, из которого оно было вызвано.

        Parameters
        ----------
        - title: str
            Заголовок окна.

        - msg: str
            Сообщение для информации.

        window: QWidget
            Окно, относительно которого выводится это окно.

        type: str
            Тип выводимого окна. Пока что доступен только тип `error`. Все
            остальное будет трактоваться как info.
        """

        box = QMessageBox(window)
        box.setWindowTitle(title)
        box.setText(msg)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        if type == set.ERROR:
            box.setIcon(QMessageBox.Icon.Critical)
            box.show()

        else:
            box.setIcon(QMessageBox.Icon.Information)
            box.exec()
