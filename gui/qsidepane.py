from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtWidgets import QLabel, QDialogButtonBox, QPushButton

OFFSET = 700


class SidePane(QLabel):
    def __init__(self, parent=None):
        super(SidePane, self).__init__(parent)
        self.parent1 = parent
        self.move(OFFSET + 80, 50)
        self.resize(250, 500)

        self.index = 0

        # buttons = QDialogButtonBox(
        #     QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
        #     Qt.Horizontal, self)
        # buttons.accepted.connect(self.send_get_move_req)
        # buttons.rejected.connect(self.send_build_req)
        # buttons.move(OFFSET + 60, 480)

        # self.texture_pix = QPixmap('brown_texture.jpg')
        self.setStyleSheet("SidePane {background-image: url(brown_texture.jpg); background-attachment: fixed; background-position: center;}")

        button = QPushButton("Buduj", parent=self.parent1)
        button.move(OFFSET + 125, 350)
        button.setEnabled(True)
        button.clicked.connect(self.parent1.send_build_req)
        button.show()

        button2 = QPushButton("Odrzuc", parent=self.parent1)
        button2.move(OFFSET + 210, 350)
        button2.setEnabled(False)
        button2.clicked.connect(self.parent1.send_build_req)
        button2.show()

        self.resources = []
        self.card = QLabel(self.parent1)

    def update_card_details(self, res):
        for r in self.resources:
            r.setParent(None)
            r.deleteLater()
        self.resources = []
        off = 0
        for r in res:
            q_res = QResource(self.parent1, res=r, location=[OFFSET + 90, 390 + off])
            off += 40
            self.resources.append(q_res)

        print("Received RES!", res)


    def set_card(self, index):
        self.index = index

        pixmap1 = QPixmap(f"cards/{index}.jpg").scaledToHeight(300)
        self.card.move(self.parent1.width() - pixmap1.width() - 20, 50)
        self.card.setPixmap(pixmap1)
        self.card.resize(self.card.pixmap().width(), self.card.pixmap().height())
        self.card.show()

        # srcImg = QImage("cards/111.jpg").scaledToHeight(100)
        # center = QPoint(srcImg.rect().center())
        # matrix = QTransform()
        # matrix.translate(center.x(), center.y())
        # matrix.rotate(90)
        # dstImg = QImage(srcImg.transformed(matrix))
        # dstPix = QPixmap().fromImage(dstImg)
        #
        # print("Qlabel")
        # a = QLabel(self.parent1)
        # a.setPixmap(dstPix)
        # a.resize(dstPix.width(), dstPix.height())
        # a.move(100, 100)
        # a.show()


class QResource(QLabel):
    def __init__(self, parent=None, res=None, location=[100, 100]):
        super(QResource, self).__init__(parent)
        self.parent1 = parent

        self.setStyleSheet("QResource {background-image: url(brown_texture.jpg); background-attachment: fixed; background-position: center;}")


        if res is None:
            return

        # src_img = QImage(f'res/{res}.png').scaledToHeight(30)
        dst_pix = QPixmap(f'res/{res}.png').scaledToHeight(30)

        self.setPixmap(dst_pix)
        self.move(location[0], location[1])
        self.show()

