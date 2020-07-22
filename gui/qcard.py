from PyQt5.QtCore import QPropertyAnimation, QRect, QPoint
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage, QTransform
from PyQt5.QtWidgets import QLabel

offsets = {'brown': (1024 - 350 - 15, 768 - 150 - 23),
           'grey': (1024 - 350 - 15, 768 - 150 - 23),
           'green': (530, 768 - 230 - 23),
           'red': (345, 768 - 150 - 23 - 80),
           'blue': (440, 768 - 150 - 23 - 80),
           'yellow': (100, 768 - 80 - 23),
           'purple': (650, 768 - 150 - 23 - 80),
           'unknown': (700, 768 - 150 - 23 - 80)}

left_offsets = {'brown': (85, 180),
           'grey': (85, 180),
           'green': (30, 70),
           'red': (170, 210),
           'blue': (170, 305),
           'yellow': (170, 405),
           'purple': (170, 500),
           'unknown': (170, 700)}

right_offsets = {'brown': (655, 120),
           'grey': (655, 120),
           'green': (600, 200),
           'red': (400, 200),
           'blue': (500, 200),
           'yellow': (300, 50),
           'purple': (100, 200),
           'unknown': (200, 200)}

next_offset = (12, 23)


class QCard(QLabel):
    def __init__(self, parent=None, index=111, location=None, owner='player', type='hand'):
        super(QCard, self).__init__(parent)
        self.index = index
        self.parent1 = parent

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(500)
        self.start_anim = QPropertyAnimation(self, b"geometry")
        self.start_anim.setDuration(1000)

        self.owner = owner
        self.type = type

        if type == 'built':
            src_img = QImage(f"cards/{index}.jpg").scaledToHeight(100)
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
                self.start_anim.setStartValue(QRect(1024 - 200, 768 - 200, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.start_anim.setEndValue(QRect(1024 - 200, 768 - 200, self.pixmap().width() * 2, self.pixmap().height() * 2))

                self.anim.setStartValue(QRect(1024 - 200, 768 - 200, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.anim.setEndValue(QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))
                self.anim.finished.connect(self.parent1.game_data.send_game_data_req)
            elif owner == 'left':
                self.start_anim.finished.connect(self.anim.start)
                self.start_anim.setStartValue(QRect(100, 300, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.start_anim.setEndValue(QRect(100, 300, self.pixmap().width() * 2, self.pixmap().height() * 2))

                self.anim.setStartValue(QRect(100, 300, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.anim.setEndValue(QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))
                self.anim.finished.connect(self.lower)
            elif owner == 'right':
                self.start_anim.finished.connect(self.anim.start)
                self.start_anim.setStartValue(QRect(500, 100, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.start_anim.setEndValue(QRect(500, 100, self.pixmap().width() * 2, self.pixmap().height() * 2))

                self.anim.setStartValue(QRect(500, 100, self.pixmap().width() * 2, self.pixmap().height() * 2))
                self.anim.setEndValue(QRect(location[0], location[1], self.pixmap().width(), self.pixmap().height()))
                self.anim.finished.connect(self.lower)


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
        if self.owner == 'player':
            src_img = QImage(f"cards/{self.index}.jpg").scaledToHeight(self.height())
            dst_pix = QPixmap().fromImage(src_img)
        if self.owner == 'left':
            src_img = QImage(f"cards/{self.index}.jpg").scaledToHeight(self.width())
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(90)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)
        if self.owner == 'right':
            src_img = QImage(f"cards/{self.index}.jpg").scaledToHeight(self.height())
            center = QPoint(src_img.rect().center())
            matrix = QTransform()
            matrix.translate(center.x(), center.y())
            matrix.rotate(180)
            dst_img = QImage(src_img.transformed(matrix))
            dst_pix = QPixmap().fromImage(dst_img)
        self.setPixmap(dst_pix)
        super(QCard, self).resizeEvent(a0)


class QPlayerDeck:
    def __init__(self, parent):
        self.parent = parent

        self.cards_built = []
        self.left_cards_built = []
        self.right_cards_built = []

        self.cards = {'brown': 0,
                      'grey': 0,
                      'green': 0,
                      'red': 0,
                      'blue': 0,
                      'yellow': 0,
                      'purple': 0,
                      'unknown': 0}

        self.left_cards = {'brown': 0,
                      'grey': 0,
                      'green': 0,
                      'red': 0,
                      'blue': 0,
                      'yellow': 0,
                      'purple': 0,
                      'unknown': 0}

        self.right_cards = {'brown': 0,
                      'grey': 0,
                      'green': 0,
                      'red': 0,
                      'blue': 0,
                      'yellow': 0,
                      'purple': 0,
                      'unknown': 0}

    def build_card(self, index, owner='player'):
        color = get_color(index)

        if owner == 'player':
            pos = offsets[color]
            card_pos = (pos[0] - self.cards[color]*next_offset[0], pos[1] - self.cards[color]*next_offset[1])
            card = QCard(self.parent, index=index, location=card_pos, owner='player', type='built')
            card.show()
            card.start_anim.start()

            card.lower()

            self.cards_built.append(card)
            self.cards[color] += 1
        elif owner == 'left':
            pos = left_offsets[color]
            card_pos = (pos[0] + self.left_cards[color] * next_offset[1], pos[1] - self.left_cards[color] * next_offset[0])

            card = QCard(self.parent, index=index, location=card_pos, owner='left', type='built')
            card.show()
            card.start_anim.start()

            # card.lower()

            self.left_cards_built.append(card)
            self.left_cards[color] += 1
        elif owner == 'right':
            pos = right_offsets[color]
            card_pos = (pos[0] + self.right_cards[color] * next_offset[0], pos[1] + self.right_cards[color] * next_offset[1])

            card = QCard(self.parent, index=index, location=card_pos, owner='right', type='built')
            card.show()
            card.start_anim.start()

            card.lower()

            self.right_cards_built.append(card)
            self.right_cards[color] += 1


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
