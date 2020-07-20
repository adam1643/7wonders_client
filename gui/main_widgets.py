from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize


class QBigWidgets(QLabel):
    def __init__(self, parent=None, location=None, size=200):
        super(QBigWidgets, self).__init__(parent)
        self.parent1 = parent
        if location is None:
            self.move((self.parent1.width() - 200) / 2, (self.parent1.height() - 300) / 2)
        else:
            self.move(location[0], location[1])
        # self.move(OFFSET + 80, 50)
        self.resize(size, size)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        self.movie = QMovie("sand.gif")
        self.movie.setScaledSize(QSize(100, 100))
        self.setMovie(self.movie)
        self.movie.setSpeed(40)

        self.lower()
        # self.lower()
        # self.lower()
        # self.lower()

    def start_waiting(self):
        self.raise_()
        self.show()
        self.movie.start()

    def stop_waiting(self):
        self.movie.stop()
        self.hide()
        self.lower()
