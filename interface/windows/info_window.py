from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont


class InfoWindow(QDialog):
    def __init__(self, message="Loading...", parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint
        )
        self.setModal(True)
        self.setWindowTitle("Aspetta...")
        self.setFixedSize(500, 200)
        self.setStyleSheet("background-color: #e1e4e6;")

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
        pixmap = QPixmap("files/icons/main_logo.png")
        image_label.setPixmap(pixmap)

        layout.addWidget(image_label)
        layout.addWidget(label)
        self.setLayout(layout)
