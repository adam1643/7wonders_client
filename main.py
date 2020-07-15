from PyQt5.QtGui import QPalette, QColor, QPixmap, QResizeEvent, QTransform, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QCheckBox, QStyleFactory, QTextEdit, QPushButton, \
    QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QLineEdit, QLabel, QSlider, QWidget, QDateTimeEdit, \
    QDialogButtonBox
from PyQt5.QtCore import Qt, QVariantAnimation, QVariant, pyqtSlot, QEasingCurve, QEventLoop, QTimer, QDateTime, \
    QPropertyAnimation, QRect, pyqtSignal

from client import queue, client
import threading
from game_data import GameData
from gui.qcard import QCard, QPlayerDeck
from gui.QLoginDialog import QLoginDialog
from gui.qwonder import QWonder
from gui.qstats import QStats
from gui.qsidepane import SidePane

OFFSET = 700


class GameGUI(QDialog):
    queue_text = pyqtSignal(int)
    wonder_signal = pyqtSignal(int)
    game_update_signal = pyqtSignal(int)
    new_move_signal = pyqtSignal(int, int, int)
    card_details_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(GameGUI, self).__init__(parent)
        self.setWindowTitle("7 CUDÓW ŚWIATA")
        QApplication.setStyle(QStyleFactory.create('windows'))
        self.setMinimumSize(1024, 768)
        self.setMaximumSize(1024, 768)
        self.setStyleSheet("background-image: url(bg.jpg); background-attachment: fixed; background-position: center;")

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.send_get_move_req)
        buttons.rejected.connect(self.send_build_req)
        buttons.move(OFFSET + 60, 480)

        self.pane = SidePane(self)

        self.cards = []
        self.set_cards([331, 332])

        self.login, self.password = self.get_login()

        self.queue_text.connect(self.update_queue)
        self.wonder_signal.connect(self.update_wonder)
        self.game_update_signal.connect(self.update_game)
        self.new_move_signal.connect(self.new_move)
        self.card_details_signal.connect(self.card_details)
        self.queue_label = None

        self.stats = QStats(self)
        self.stats.move(0, 0)
        self.stats.show()

        self.player_deck = QPlayerDeck(self)

    @staticmethod
    def send_game_data_req():
        game_data.send_game_data_req()

    def send_get_move_req(self):
        game_data.send_get_move_req()

    def send_build_req(self):
        game_data.send_build_req(self.pane.index)

    def send_card_details(self, index):
        game_data.send_card_details_req(index)

    def get_login(self):
        login, password, ok = QLoginDialog.get_login_data()
        print(login, password)
        return login, password

    def new_move(self, player, left, right):
        print("Built IDs", player, left, right)
        self.player_deck.build_card(player)

    def card_details(self, res):
        self.pane.update_card_details(res)

    def update_game(self, index):
        print("Update game")
        left_id = game_data.left_neighbor[0]
        right_id = game_data.right_neighbor[0]

        wonder = QWonder(self, left_id, owner='left')
        wonder.move(20, 200)
        wonder.show()
        self.left_wonder = wonder

        # self.set_left_cards(game_data.left_neighbor[1])
        wonder = QWonder(self, right_id, owner='right')
        wonder.move(400, 50)
        wonder.show()
        self.right_wonder = wonder

        self.set_right_cards(game_data.right_neighbor[1])

        self.set_cards(game_data.cards)
        self.stats.update_data(vp=game_data.vp, money=game_data.money, military=game_data.military, ready=game_data.ready)

    def set_right_cards(self, no):
        self.right_cards = []
        off = 0
        for _ in range(no):
            card = QCard(self, 'back1')
            pixmap = QPixmap(f"cards/back1.jpg").scaledToHeight(100)
            card.setPixmap(pixmap)
            card.move(50 + off, 30)
            card.resize(pixmap.width(), pixmap.height())
            card.show()  # You were missing this.
            off += 10
            self.right_cards.append(card)

    def set_big(self, index):
        self.pane.set_card(index)
        self.send_card_details(index)

        # self.player_deck.build_card(111)
        # self.player_deck.build_card(121)
        # self.player_deck.build_card(131)
        # self.player_deck.build_card(132)
        #
        # self.player_deck.build_card(141)
        # self.player_deck.build_card(142)
        # self.player_deck.build_card(151)
        # self.player_deck.build_card(152)
        # self.player_deck.build_card(161)
        # self.player_deck.build_card(162)

    def update_queue(self, no=0):
        print("updating queue")
        # if no != 3:
        #     self.queue_label = QLabel(self)
        #     self.queue_label.setText(f'{no}/3 players in queue')
        #     self.queue_label.move(0,0)
        #     self.queue_label.show()
        self.stats.update_data(ready=no)

    def update_wonder(self, index):
        wonder = QWonder(self, index)
        pixmap = QPixmap(f"wonders/{index}.jpeg").scaledToHeight(150)
        wonder.setPixmap(pixmap)
        wonder.move(self.width() - pixmap.width(), self.height() - pixmap.height())
        wonder.resize(pixmap.width(), pixmap.height())
        wonder.show()
        self.wonder = wonder

    def set_cards(self, ids):
        for card in self.cards:
            card.setParent(None)
            card.deleteLater()

        self.cards = []
        self.wonders = []
        off = 200
        for index in ids:
            card = QCard(self, index)
            pixmap = QPixmap(f"cards/{index}.jpg").scaledToHeight(150)
            card.set_size(pixmap.width(), pixmap.height(), 10 + off, self.height() - 150)
            card.setPixmap(pixmap)
            card.move(10 + off, self.height() - 150)
            card.resize(pixmap.width(), pixmap.height())
            card.show()  # You were missing this.
            # off += pixmap.width() + 3
            off += 50
            self.cards.append(card)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.png'))
    gui = GameGUI()
    game_data = GameData(gui)
    if len(gui.login) > 0:
        game_data.login = gui.login
    game_data.send_game_data_req()

    network_client = threading.Thread(target=client, args=(game_data,))
    network_client.start()

    gui.show()
    app.exec_()


# class AnimationLabel(QLabel):
#     def __init__(self, *args, **kwargs):
#         QLabel.__init__(self, *args, **kwargs)
#         self.animation = QVariantAnimation()
#         self.animation.valueChanged.connect(self.changeColor)
#
#     @pyqtSlot(QVariant)
#     def changeColor(self, color):
#         palette = self.palette()
#         palette.setColor(QPalette.WindowText, color)
#         self.setPalette(palette)
#
#     def startFadeIn(self):
#         self.animation.stop()
#         self.animation.setStartValue(QColor(0, 0, 0, 0))
#         self.animation.setEndValue(QColor(0, 0, 0, 255))
#         self.animation.setDuration(2000)
#         self.animation.setEasingCurve(QEasingCurve.InBack)
#         self.animation.start()
#
#     def startFadeOut(self):
#         self.animation.stop()
#         self.animation.setStartValue(QColor(0, 0, 0, 255))
#         self.animation.setEndValue(QColor(0, 0, 0, 0))
#         self.animation.setDuration(2000)
#         self.animation.setEasingCurve(QEasingCurve.OutBack)
#         self.animation.start()
#
#     def startAnimation(self):
#         self.startFadeIn()
#         loop = QEventLoop()
#         self.animation.finished.connect(loop.quit)
#         loop.exec_()
#         QTimer.singleShot(2000, self.startFadeOut)
#
# class Widget(QWidget):
#     def __init__(self):
#         super().__init__()
#         lay = QVBoxLayout(self)
#         self.greeting_text = AnimationLabel("greeting_text")
#         self.greeting_text.setStyleSheet("font : 45px; font : bold; font-family : HelveticaNeue-UltraLight")
#         lay.addWidget(self.greeting_text)
#         btnFadeIn = QPushButton("fade in")
#         btnFadeOut = QPushButton("fade out")
#         btnAnimation = QPushButton("animation")
#         lay.addWidget(btnFadeIn)
#         lay.addWidget(btnFadeOut)
#         lay.addWidget(btnAnimation)
#         btnFadeIn.clicked.connect(self.greeting_text.startFadeIn)
#         btnFadeOut.clicked.connect(self.greeting_text.startFadeOut)
#         btnAnimation.clicked.connect(self.greeting_text.startAnimation)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Widget()
#     ex.show()
#     sys.exit(app.exec_())




