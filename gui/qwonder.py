from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QResizeEvent, QPixmap, QImage, QTransform
from PyQt5.QtWidgets import QLabel


class QWonder(QLabel):
    def __init__(self, parent=None, index=1, owner='player'):
        super(QWonder, self).__init__(parent)
        self.index = index
        self.parent1 = parent

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

    def mousePressEvent(self, ev) -> None:
        self.parent1.set_wonder(self.index)
        super(QWonder, self).mousePressEvent(ev)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super(QWonder, self).resizeEvent(a0)
