from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QTransform, QColor, QMovie
from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QPushButton

OFFSET = 700


class SidePane(QLabel):
    def __init__(self, parent=None):
        super(SidePane, self).__init__(parent)
        self.parent1 = parent
        self.move(OFFSET + 80, 50)
        self.resize(250, 500)

        self.index = 0

        self.setStyleSheet("SidePane {background-image: url(brown_texture.jpg); background-attachment: fixed; background-position: center;}")

        button = QPushButton("Buduj", parent=self.parent1)
        button.move(OFFSET + 125, 350)
        button.setEnabled(True)
        button.clicked.connect(self.parent1.send_build_req)
        button.show()

        button2 = QPushButton("Odrzuc", parent=self.parent1)
        button2.move(OFFSET + 210, 350)
        button2.setEnabled(True)
        button2.clicked.connect(self.parent1.send_build_req_discard)
        button2.show()

        self.resources = []
        self.checkmarks = []
        self.card = QLabel(self.parent1)

    def update_card_details(self, res, availability, upgrade=False):
        for r in self.resources:
            r.setParent(None)
            r.deleteLater()
        for line in self.checkmarks:
            for c in line:
                c.setParent(None)
                c.deleteLater()

        self.resources = []
        self.checkmarks = []

        print(availability)

        if upgrade is True:
            q_upgrade = QUpgradeIcon(self.parent1, location=[OFFSET + 130, 390 + 10])
            self.resources.append(q_upgrade)
            return

        off = 0
        for r, c in zip(res, availability):
            q_res = QResource(self.parent1, res=r, location=[OFFSET + 90, 390 + off])
            self.resources.append(q_res)
            self.checkmarks.append([])

            if c == 'own' or c == 'none' or c == 'left' or c == 'right':
                check = c
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off])
                self.checkmarks[-1].append(q_check)
            if c == 'both':
                print("BOTH")
                check = 'left'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
                check = 'right'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
            if c == 'all':
                check = 'left'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
                check = 'right'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
                check = 'down'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
            if c == 'left_own':
                check = 'left'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
                check = 'down'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
            if c == 'right_own':
                check = 'right'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
                check = 'down'
                q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)

            off += 20

    def set_card(self, index):
        self.index = index

        pixmap1 = QPixmap(f"cards/{index}.jpg").scaledToHeight(300)
        self.card.move(self.parent1.width() - pixmap1.width() - 20, 50)
        self.card.setPixmap(pixmap1)
        self.card.resize(self.card.pixmap().width(), self.card.pixmap().height())
        self.card.show()

    def set_wonder(self, index):
        pixmap1 = QPixmap(f'wonders/{index}.jpeg').scaledToHeight(100)
        self.card.move(self.parent1.width() - pixmap1.width() - 20, 50)
        self.card.setPixmap(pixmap1)
        self.card.resize(self.card.pixmap().width(), self.card.pixmap().height())
        self.card.show()

    def get_chosen(self):
        chosen = ['none' for _ in self.checkmarks]
        for idx, line in enumerate(self.checkmarks):
            if len(line) == 1:
                if line[0].highlighted is True:
                    chosen[idx] = line[0].check
            if len(line) == 2:
                if line[0].highlighted is True:
                    chosen[idx] = line[0].check
                if line[1].highlighted is True:
                    chosen[idx] = line[1].check

        return chosen


class QResource(QLabel):
    def __init__(self, parent=None, res=None, location=[100, 100]):
        super(QResource, self).__init__(parent)
        self.parent1 = parent
        self.res = res

        # self.setStyleSheet("QResource {background-color: transparent;}")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        if res is None:
            return

        src_img = QImage(f'res/{res}.png').scaledToHeight(30)
        dst_pix = QPixmap(f'res/{res}.png').scaledToHeight(30)

        self.setPixmap(dst_pix)
        self.move(location[0], location[1])
        self.show()


class QCheckmark(QLabel):
    def __init__(self, parent=None, check='none', location=(100, 100), line=None):
        super(QCheckmark, self).__init__(parent)
        self.parent1 = parent
        self.check = check

        self.line = line

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        if check == 'own':
            src_img = QImage(f'check_ok.png').scaledToHeight(20)
            dst_pix = QPixmap(f'check_ok.png').scaledToHeight(20)
        elif check == 'none':
            src_img = QImage(f'check_wrong.png').scaledToHeight(20)
            dst_pix = QPixmap(f'check_wrong.png').scaledToHeight(20)
        elif check == 'left':
            src_img = QImage(f'icons/left.png').scaledToHeight(20)
            dst_pix = QPixmap(f'icons/left.png').scaledToHeight(20)
        elif check == 'right':
            src_img = QImage(f'icons/right.png').scaledToHeight(20)
            dst_pix = QPixmap(f'icons/right.png').scaledToHeight(20)
        elif check == 'down':
            dst_pix = QPixmap(f'icons/down.png').scaledToHeight(20)

        self.setPixmap(dst_pix)
        self.move(location[0], location[1])
        self.show()

        self.highlighted = False

    def set_highlighted(self, status):
        self.highlighted = status
        dst_pix = None
        if status is True:
            if self.line is not None:
                for c in self.line:
                    c.set_highlighted(False)
            if self.check == 'left':
                dst_pix = QPixmap(f'icons/left-yellow.png').scaledToHeight(20)
            if self.check == 'right':
                dst_pix = QPixmap(f'icons/right-yellow.png').scaledToHeight(20)
            if self.check == 'down':
                dst_pix = QPixmap(f'icons/down-yellow.png').scaledToHeight(20)
        else:
            if self.check == 'left':
                dst_pix = QPixmap(f'icons/left.png').scaledToHeight(20)
            if self.check == 'right':
                dst_pix = QPixmap(f'icons/right.png').scaledToHeight(20)
            if self.check == 'down':
                dst_pix = QPixmap(f'icons/down.png').scaledToHeight(20)
        if dst_pix is not None:
            self.setPixmap(dst_pix)

    def mousePressEvent(self, event):
        self.set_highlighted(True)
        super(QCheckmark, self).mousePressEvent(event)


class QUpgradeIcon(QLabel):
    def __init__(self, parent=None, location=(100, 100)):
        super(QUpgradeIcon, self).__init__(parent)
        self.parent1 = parent

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        dst_pix = QPixmap(f'icons/upgrade.png').scaledToHeight(100)
        self.setPixmap(dst_pix)

        self.move(location[0], location[1])
        self.show()
