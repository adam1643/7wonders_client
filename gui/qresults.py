from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QDialogButtonBox, QLabel
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt, QPoint


class QResults(QDialog):
    def __init__(self, parent=None):
        super(QResults, self).__init__(parent)

        self.setWindowTitle("WALKA")

        self.resize(300, 300)
        # self.setStyleSheet("QResults {background-image: url(brown_texture.jpg); background-attachment: fixed; background-position: center;}")

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.move(self.width()//2 - 40, self.height() - 40)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def set_battle(parent=None, player=[0, 0], left=[0, 0], right=[0, 0]):
        dialog = QResults(parent)
        for idx, battle in enumerate(player):
            if battle > 0:
                QWin(dialog, location=[dialog.width()//2 - 50 + idx*50, dialog.height() - 110])
            elif battle < 0:
                QLose(dialog, location=[dialog.width()//2 - 50 + idx*50, dialog.height() - 110])

        for idx, battle in enumerate(left):
            if battle > 0:
                QWin(dialog, location=[10, dialog.height()//2 - 60 + idx*50])
            elif battle < 0:
                QLose(dialog, location=[10, dialog.height()//2 - 60 + idx*50])

        for idx, battle in enumerate(right):
            if battle > 0:
                QWin(dialog, location=[dialog.width()//2 - 50 + idx*50, 10])
            elif battle < 0:
                QLose(dialog, location=[dialog.width()//2 - 50 + idx*50, 10])
        dialog.exec_()


class QLose(QLabel):
    def __init__(self, parent=None, location=[100, 100]):
        super(QLose, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        pixmap = QPixmap("icons/loses.png").scaledToHeight(80)
        self.setPixmap(pixmap)
        self.move(location[0], location[1])
        self.show()


class QWin(QLabel):
    def __init__(self, parent=None, location=[100, 100]):
        super(QWin, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        pixmap = QPixmap("icons/wins.png").scaledToHeight(80)
        self.setPixmap(pixmap)
        self.move(location[0], location[1])
        self.show()
