from PyQt5.QtCore import QPoint, QRect, QPropertyAnimation
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage, QTransform
from PyQt5.QtWidgets import QLabel


class QWonder(QLabel):
    def __init__(self, parent=None, index=1, owner='player'):
        super(QWonder, self).__init__(parent)
        self.index = index
        self.parent1 = parent
        self.level = 0
        self.owner = owner

        if owner == 'player':
            pass
        elif owner == 'left':
            src_img = QImage(f"wonders/{index}.jpeg").scaledToHeight(150)
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(90)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)

            self.setPixmap(dst_pix)
        elif owner == 'right':
            src_img = QImage(f"wonders/{index}.jpeg").scaledToHeight(150)
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(180)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)

            self.setPixmap(dst_pix)
            self.lower()

    def upgrade(self, age=1):
        self.level += 1
        if self.owner == 'player':
            c = QBackCard(self.parent1, owner=self.owner, location=[self.x() + 25 + 102*(self.level-1), self.y() + self.height() - 30], level=self.level)
        elif self.owner == 'left':
            c = QBackCard(self.parent1, owner=self.owner, location=[self.x() - 30, self.y() + 30 + 102*(self.level-1)], level=self.level)
        elif self.owner == 'right':
            c = QBackCard(self.parent1, owner=self.owner, location=[self.x() + 25 + 102*(self.level-1), self.y() - 30], level=self.level)
        c.anim.start()

    def mousePressEvent(self, ev) -> None:
        self.parent1.set_wonder(self.index)
        super(QWonder, self).mousePressEvent(ev)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super(QWonder, self).resizeEvent(a0)


class QBackCard(QLabel):
    def __init__(self, parent=None, index=1, location=None, owner='player', level=1):
        super(QBackCard, self).__init__(parent)
        self.index = index
        self.parent1 = parent
        self.level = level

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(500)
        self.start_anim = QPropertyAnimation(self, b"geometry")
        self.start_anim.setDuration(1000)

        self.owner = owner

        src_img = QImage(f"cards/back{index}.jpg").scaledToHeight(130)
        if owner == 'player':
            dst_pix = QPixmap().fromImage(src_img)
        elif owner == 'left':
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(90)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)
        elif owner == 'right':
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(180)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)
        self.setPixmap(dst_pix)
        if location is not None:
            if owner == 'player':
                self.raise_()
                self.start_anim.finished.connect(self.anim.start)
                self.start_anim.setStartValue(
                    QRect(1024 - 200, 768 - 200, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.start_anim.setEndValue(
                    QRect(1024 - 200, 768 - 200, self.pixmap().width() * 2, self.pixmap().height() * 2))

                self.anim.setStartValue(
                    QRect(1024 - 200, 768 - 200, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.anim.setEndValue(
                    QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))
                self.anim.finished.connect(self.lower)
            elif owner == 'left':
                self.start_anim.finished.connect(self.anim.start)
                self.start_anim.setStartValue(
                    QRect(100, 300, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.start_anim.setEndValue(QRect(100, 300, self.pixmap().width() * 2, self.pixmap().height() * 2))

                self.anim.setStartValue(QRect(100, 300, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.anim.setEndValue(
                    QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))
                self.anim.finished.connect(self.lower)
            elif owner == 'right':
                self.start_anim.finished.connect(self.anim.start)
                self.start_anim.setStartValue(
                    QRect(500, 100, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.start_anim.setEndValue(QRect(500, 100, self.pixmap().width() * 2, self.pixmap().height() * 2))

                self.anim.setStartValue(QRect(500, 100, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.anim.setEndValue(
                    QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))
                self.anim.finished.connect(self.lower)

        self.show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self.owner == 'player':
            src_img = QImage(f"cards/back{self.index}.jpg").scaledToHeight(self.height())
            dst_pix = QPixmap().fromImage(src_img)
        if self.owner == 'left':
            src_img = QImage(f"cards/back{self.index}.jpg").scaledToHeight(self.width())
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(90)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)
        if self.owner == 'right':
            src_img = QImage(f"cards/back{self.index}.jpg").scaledToHeight(self.height())
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(180)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)
        self.setPixmap(dst_pix)
        super(QBackCard, self).resizeEvent(a0)