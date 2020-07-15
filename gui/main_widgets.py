from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel


class QBigWidgets(QLabel):
    def __init__(self, parent=None):
        super(QBigWidgets, self).__init__(parent)
        self.parent1 = parent
        self.move((self.parent1.width() - 300) / 2, (self.parent1.height() - 300) / 2)
        # self.move(OFFSET + 80, 50)
        self.resize(300, 300)

        self.movie = QMovie("sand.gif")
        self.setMovie(self.movie)
        self.movie.setSpeed(40)

    def start_waiting(self):
        self.show()
        self.movie.start()

    def stop_waiting(self):
        self.movie.stop()
        self.hide()
