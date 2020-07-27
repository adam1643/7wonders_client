from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QDialogButtonBox, QLabel
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt, QPoint


class QError(QDialog):
    def __init__(self, parent=None, code=1):
        super(QError, self).__init__(parent)

        self.setWindowTitle("BŁĄD")

        self.resize(300, 300)
        self.setStyleSheet("QError {background-image: url(brown_texture.jpg); background-attachment: fixed; background-position: center;}")

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.move(self.width()//2 - 40, self.height() - 40)

        self.label = QLabel(parent=self)
        self.label.resize(200, 200)
        self.label.move(50, 50)
        self.label.show()
        self.label.setWindowFlags(Qt.FramelessWindowHint)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background:transparent;")
        if code == 10:
            self.label.setText("Brak potrzebnych surowcow!")
