from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont

from settings import settings as sett


class InfoWindow(QDialog):
    def __init__(self, message=sett.LOADING_IT, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        self.setModal(True)
        self.setWindowTitle(sett.WAIT_IT)
        self.setFixedSize(
            sett.INFO_WINDOW_WIDTH,
            sett.INFO_WINDOW_HEIGHT
        )

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        label.setFont(font)

        image_label = QLabel()
        image_label.setScaledContents(True)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(sett.MAIN_LOGO_PATH)
        image_label.setPixmap(pixmap)

        layout.addWidget(image_label)
        layout.addWidget(label)
        self.setLayout(layout)
