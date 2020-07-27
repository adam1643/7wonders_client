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

        self.button_build = QPushButton("Buduj", parent=self.parent1)
        self.button_build.move(OFFSET + 100, 350)
        self.button_build.setEnabled(True)
        self.button_build.clicked.connect(self.parent1.send_build_req)
        self.button_build.show()

        self.button_discard = QPushButton("Odrzuc", parent=self.parent1)
        self.button_discard.move(OFFSET + 235, 350)
        self.button_discard.setEnabled(True)
        self.button_discard.clicked.connect(self.parent1.send_build_req_discard)
        self.button_discard.show()

        self.button_wonder = QPushButton("Cud", parent=self.parent1)
        self.button_wonder.move(OFFSET + 180, 350)
        self.button_wonder.setEnabled(True)
        self.button_wonder.setFixedSize(50, self.button_discard.height())
        self.button_wonder.clicked.connect(lambda: self.parent1.set_wonder(1))
        self.button_wonder.show()

        self.resources = []
        self.checkmarks = []
        self.card = QLabel(self.parent1)

        self.upgrade_icon = QUpgradeIcon(self.parent1, location=[OFFSET + 130, 390 + 10])

    def set_build_button_enabled(self, status):
        self.button_build.setEnabled(status)

    def set_dicard_button_enabled(self, status):
        self.button_discard.setEnabled(status)

    def update_card_details(self, res, availability, upgrade=False):
        for resource, checkmarks in zip(self.resources, self.checkmarks):
            resource.setParent(None)
            resource.deleteLater()
            for ch in checkmarks:
                ch.setParent(None)
                ch.deleteLater()
        self.resources = []
        self.checkmarks = []

        if upgrade is True:
            self.upgrade_icon.show()
            return
        else:
            self.upgrade_icon.hide()

        off = 0
        for r, c in zip(res, availability):
            q_res = QResource(self.parent1, res=r, location=[OFFSET + 90, 390 + off])
            self.resources.append(q_res)
            self.checkmarks.append([])

            if c in ['none', 'own', 'down']:
                q_check = QCheckmark(self.parent1, check=c, location=[OFFSET + 90 + 40, 395 + off])
                self.checkmarks[-1].append(q_check)
            if c in ['left', 'both', 'all', 'left_own']:
                q_check = QCheckmark(self.parent1, check='left', location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
            if c in ['all', 'left_own', 'right_own']:
                q_check = QCheckmark(self.parent1, check='down', location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)
            if c in ['right', 'both', 'all', 'right_own']:
                q_check = QCheckmark(self.parent1, check='right', location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
                self.checkmarks[-1].append(q_check)

            # if c == 'own' or c == 'none' or c == 'left' or c == 'right':
            #     check = c
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off])
            #     self.checkmarks[-1].append(q_check)
            # if c == 'both':
            #     check = 'left'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            #     check = 'right'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            # if c == 'all':
            #     check = 'left'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            #     check = 'right'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            #     check = 'down'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            # if c == 'left_own':
            #     check = 'left'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            #     check = 'down'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            # if c == 'right_own':
            #     check = 'right'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 40, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            #     check = 'down'
            #     q_check = QCheckmark(self.parent1, check=check, location=[OFFSET + 90 + 40 + 20, 395 + off], line=self.checkmarks[-1])
            #     self.checkmarks[-1].append(q_check)
            off += 20

    def set_card(self, index):
        self.index = index

        pixmap1 = QPixmap(f"cards/{index}.jpg").scaledToHeight(300)
        self.card.move(self.parent1.width() - pixmap1.width() - 20, 50)
        self.card.setPixmap(pixmap1)
        self.card.resize(self.card.pixmap().width(), self.card.pixmap().height())
        self.card.show()

    def set_wonder(self, index):
        self.index = 1
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

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        if res is None:
            return

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
        self.hide()
