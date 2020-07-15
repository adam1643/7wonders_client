from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage
from PyQt5.QtWidgets import QLabel

offsets = {'brown': (1024 - 350 - 15, 768 - 150 - 23),
           'grey': (1024 - 350 - 15, 768 - 150 - 23),
           'green': (250, 768 - 150 - 23 - 100),
           'red': (350, 768 - 150 - 23 - 100),
           'blue': (450, 768 - 150 - 23 - 100),
           'yellow': (550, 768 - 150 - 23 - 100),
           'purple': (650, 768 - 150 - 23 - 100),
           'unknown': (700, 768 - 150 - 23 - 100)}

next_offset = (15, 23)


class QCard(QLabel):
    def __init__(self, parent=None, index=111, location=None, owner='player', type='hand'):
        super(QCard, self).__init__(parent)
        self.index = index
        self.parent1 = parent

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(3000)

        self.owner = owner
        self.type = type

        if type == 'built':
            if owner == 'player':
                src_img = QImage(f"cards/{index}.jpg").scaledToHeight(150)
                dst_pix = QPixmap().fromImage(src_img)
                self.setPixmap(dst_pix)
        if location is not None:
            self.anim.setStartValue(QRect(300, 400, self.pixmap().width() * 2, self.pixmap().height() * 2))
            self.anim.setEndValue(QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))

        self.anim.finished.connect(lambda: print("Finished animation"))

    def mousePressEvent(self, ev) -> None:
        self.parent1.set_big(self.index)
        self.parent1.send_game_data_req()
        super(QCard, self).mousePressEvent(ev)

    def set_size(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y

        self.anim_enter = QPropertyAnimation(self, b"geometry")
        self.anim_leave = QPropertyAnimation(self, b"geometry")

    def enterEvent(self, event):
        if self.underMouse():
            print('Enter')
            if self.owner == 'player' and self.type == 'hand':
                self.anim_leave.stop()
                self.anim_enter.setDuration(200)
                self.anim_enter.setStartValue(QRect(self.pos().x(), self.pos().y(), self.pixmap().width(), self.pixmap().height()))
                self.anim_enter.setEndValue(QRect(self.x - 30, self.y - 150, 130, 200))
                self.anim_enter.start()
            # self.parent1.set_big(self.index)

        return super(QCard, self).enterEvent(event)

    def leaveEvent(self, event):
        if self.owner == 'player' and self.type == 'hand':
            self.anim_enter.stop()
            self.anim_leave.setDuration(200)
            self.anim_leave.setStartValue(
                QRect(self.pos().x(), self.pos().y(), self.pixmap().width(), self.pixmap().height()))
            self.anim_leave.setEndValue(QRect(self.x, self.y, self.w, self.h))
            self.anim_leave.start()

        return super(QCard, self).leaveEvent(event)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        pixmap1 = QPixmap(f"cards/{self.index}.jpg").scaledToHeight((self.height()))
        self.setPixmap(pixmap1)
        super(QCard, self).resizeEvent(a0)


class QPlayerDeck:
    def __init__(self, parent):
        self.parent = parent

        self.cards_built = []

        self.cards = {'brown': 0,
                      'grey': 0,
                      'green': 0,
                      'red': 0,
                      'blue': 0,
                      'yellow': 0,
                      'purple': 0,
                      'unknown': 0}
        pass

    def build_card(self, index):
        color = get_color(index)

        pos = offsets[color]
        card_pos = (pos[0] - self.cards[color]*next_offset[0], pos[1] - self.cards[color]*next_offset[1])
        card = QCard(self.parent, index=index, location=card_pos, owner='player', type='built')
        card.show()
        card.anim.start()

        card.lower()

        self.cards_built.append(card)
        self.cards[color] += 1


def get_color(index):
    color_type = (index // 10) % 10
    if color_type == 1:
        return 'brown'
    elif color_type == 2:
        return 'brown'
    elif color_type == 3:
        return 'blue'
    elif color_type == 4:
        return 'red'
    elif color_type == 5:
        return 'yellow'
    elif color_type == 6:
        return 'green'
    elif color_type == 7:
        return 'purple'
    else:
        return 'unknown'
