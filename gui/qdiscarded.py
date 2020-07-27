from PyQt5.QtCore import QRect, QPropertyAnimation
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage
from PyQt5.QtCore import Qt


class QDiscarded(QDialog):
    def __init__(self, parent=None, codes=[]):
        super(QDiscarded, self).__init__(parent)

        self.setWindowTitle("KARTY ODRZUCONE")

        self.resize(600, 500)
        self.setStyleSheet("QDiscarded {background-image: url(brown_texture.jpg); background-attachment: fixed; background-position: center;}")

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.move(self.width()//2 - 40, self.height() - 40)

        self.card = QLabel(self)
        self.selected = 0

        self.cards = []
        for idx, card_id in enumerate(codes):
            location = [30 + 70 * (idx % 5), 50 + 120 * (idx // 5)]
            card = QDiscardedCard(self, index=card_id, location=location)
            card.show()
            self.cards.append(card)
        self.exec_()

    def set_card(self, index):
        self.selected = index
        pixmap1 = QPixmap(f"cards/{index}.jpg").scaledToHeight(300)
        self.card.move(self.width() - pixmap1.width() - 10, 50)
        self.card.setPixmap(pixmap1)
        self.card.resize(self.card.pixmap().width(), self.card.pixmap().height())
        self.card.show()


class QDiscardedCard(QLabel):
    def __init__(self, parent=None, index=111, location=None):
        super(QDiscardedCard, self).__init__(parent)
        self.index = index
        self.parent1 = parent

        src_img = QImage(f"cards/{index}.jpg").scaledToHeight(100)
        dst_pix = QPixmap().fromImage(src_img)
        self.setPixmap(dst_pix)
        if location is not None:
            self.move(location[0], location[1])

        self.anim_enter = QPropertyAnimation(self, b"geometry")
        self.anim_leave = QPropertyAnimation(self, b"geometry")

        self.x, self.y, self.w, self.h = location[0], location[1], self.pixmap().width(), self.pixmap().height()

    def mousePressEvent(self, ev) -> None:
        self.parent1.set_card(self.index)
        super(QDiscardedCard, self).mousePressEvent(ev)

    def enterEvent(self, event):
        if self.underMouse():
            self.anim_leave.stop()
            self.anim_enter.setDuration(200)
            self.anim_enter.setStartValue(QRect(self.pos().x(), self.pos().y(), self.pixmap().width(), self.pixmap().height()))
            self.anim_enter.setEndValue(QRect(self.x - 30, self.y - 90, 110, 170))
            self.anim_enter.start()

        return super(QDiscardedCard, self).enterEvent(event)

    def leaveEvent(self, event):
        self.anim_enter.stop()
        self.anim_leave.setDuration(200)
        self.anim_leave.setStartValue(
            QRect(self.pos().x(), self.pos().y(), self.pixmap().width(), self.pixmap().height()))
        self.anim_leave.setEndValue(QRect(self.x, self.y, self.w, self.h))
        self.anim_leave.start()

        return super(QDiscardedCard, self).leaveEvent(event)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        src_img = QImage(f"cards/{self.index}.jpg").scaledToHeight(self.height())
        dst_pix = QPixmap().fromImage(src_img)
        self.setPixmap(dst_pix)
        super(QDiscardedCard, self).resizeEvent(a0)
