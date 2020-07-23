from PyQt5.QtGui import QPalette, QColor, QPixmap, QResizeEvent, QTransform, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QCheckBox, QStyleFactory, QTextEdit, QPushButton, \
    QGroupBox, QVBoxLayout, QHBoxLayout, QRadioButton, QLineEdit, QLabel, QSlider, QWidget, QDateTimeEdit, \
    QDialogButtonBox
from PyQt5.QtCore import Qt, QVariantAnimation, QVariant, pyqtSlot, QEasingCurve, QEventLoop, QTimer, QDateTime, \
    QPropertyAnimation, QRect, pyqtSignal

# from client import queue, client
from http_client import queue, client
import threading
from game_data import GameData
from gui.main_widgets import QBigWidgets
from gui.qcard import QCard, QPlayerDeck
from gui.QLoginDialog import QLoginDialog
from gui.qresults import QResults
from gui.qwonder import QWonder
from gui.qstats import QStats
from gui.qsidepane import SidePane
from gui.topbar import QTopBar

OFFSET = 700


class GameGUI(QDialog):
    queue_text = pyqtSignal(list)
    wonder_signal = pyqtSignal(int)
    game_update_signal = pyqtSignal(int)
    first_game_update_signal = pyqtSignal(list, list, list)
    new_move_signal = pyqtSignal(int, int, int, list)
    card_details_signal = pyqtSignal(list, list, bool)
    end_age_signal = pyqtSignal(list, list, list)

    def __init__(self, parent=None, game_data=None):
        super(GameGUI, self).__init__(parent)
        self.setWindowTitle("7 CUDÓW ŚWIATA")
        QApplication.setStyle(QStyleFactory.create('windows'))
        self.setMinimumSize(1024, 768)
        self.setMaximumSize(1024, 768)
        self.setStyleSheet("background-image: url(bg.jpg); background-attachment: fixed; background-position: center;")

        self.pane = SidePane(self)

        self.cards = []
        self.set_cards([331, 332])

        self.login, self.password = self.get_login()

        self.queue_text.connect(self.update_queue)
        self.wonder_signal.connect(self.update_wonder)
        self.game_update_signal.connect(self.update_game)
        self.first_game_update_signal.connect(self.first_update_game)
        self.new_move_signal.connect(self.new_move)
        self.card_details_signal.connect(self.card_details)
        self.end_age_signal.connect(self.end_age)
        self.queue_label = None

        self.stats = QStats(self)
        self.stats.move(0, 0)
        self.stats.show()

        self.player_deck = QPlayerDeck(self)

        self.topbar = QTopBar(self)

        self.big_widgets = QBigWidgets(self, location=(800, 630), size=100)
        self.left_wait = QBigWidgets(self, location=(45, 330), size=100)
        self.right_wait = QBigWidgets(self, location=(520, 80), size=100)

        self.game_data = game_data
        self.wonder, self.left_wonder, self.right_wonder = None, None, None

    @staticmethod
    def send_game_data_req():
        game_data.send_game_data_req()

    def send_get_move_req(self):
        game_data.send_get_move_req()

    def send_build_req(self):
        game_data.send_build_req(self.pane.index, self.pane.get_chosen())
        self.big_widgets.start_waiting()

    def send_build_req_discard(self):
        game_data.send_build_req(self.pane.index, self.pane.get_chosen(), discard=True)
        self.big_widgets.start_waiting()

    def send_card_details(self, index):
        game_data.send_card_details_req(index)

    def send_wonder_details(self, index):
        game_data.send_wonder_details_req(index)

    def get_login(self):
        login, password, ok = QLoginDialog.get_login_data()
        print(login, password)
        return login, password

    def new_move(self, player, left, right, money_delta=[]):
        print("Built IDs", player, left, right)
        self.big_widgets.stop_waiting()
        self.left_wait.stop_waiting()
        self.right_wait.stop_waiting()
        self.player_deck.build_card(player)

        if len(money_delta) > 0:
            self.topbar.money_delta(money_delta)

    def card_details(self, res, availability, upgrade=False):
        self.pane.update_card_details(res, availability, upgrade)

    def update_game(self, index):
        print("Update game")
        left_id = game_data.left_neighbor[0]
        right_id = game_data.right_neighbor[0]

        if self.left_wonder is None:
            wonder = QWonder(self, left_id, owner='left')
            wonder.move(20, 200)
            wonder.show()
            self.left_wonder = wonder

        if self.right_wonder is None:
            wonder = QWonder(self, right_id, owner='right')
            wonder.move(400, 50)
            wonder.show()
            self.right_wonder = wonder

        self.set_right_cards(game_data.right_neighbor[1])

        self.set_cards(game_data.cards)
        self.stats.update_data(vp=game_data.vp, money=game_data.money, military=game_data.military, ready=game_data.ready)

        a, b, c, d = game_data.top_data
        print("DATA", a, b, c, d)
        self.topbar.update_data(a, b, c, d)

    def first_update_game(self, built, left, right):
        print('first_update')
        for i in built:
            self.player_deck.build_card(i)
        for i in left:
            self.player_deck.build_card(i, owner='left')
        for i in right:
            self.player_deck.build_card(i, owner='right')

    def set_right_cards(self, no):
        self.right_cards = []
        off = 0

    def set_big(self, index):
        self.pane.set_card(index)
        self.send_card_details(index)

        cards = [111, 112, 113, 121, 122, 123, 131, 132, 133, 141, 142, 143, 151, 152, 153, 161, 162, 163]

        # for c in cards:
        #     self.player_deck.build_card(c)
        #     self.player_deck.build_card(c, owner='left')
        #     self.player_deck.build_card(c, owner='right')

    def end_age(self, player, left, right):
        QResults.set_battle(self, player, left, right)

    def set_wonder(self, index):
        self.send_wonder_details(index)
        self.pane.set_wonder(index)

        self.wonder.upgrade()
        self.left_wonder.upgrade()
        self.right_wonder.upgrade()
        # QResults.set_battle(self, player=[-1, -1], left=[-1, 1], right=[-1, 1])

    def update_queue(self, data=[0, False, False, False]):
        if data[1] is True:
            self.big_widgets.start_waiting()
        if data[2] is True:
            self.left_wait.start_waiting()
        if data[3] is True:
            self.right_wait.start_waiting()
        self.stats.update_data(ready=data[0])

    def update_wonder(self, index):
        if self.wonder is None:
            wonder = QWonder(self, index)
            pixmap = QPixmap(f"wonders/{index}.jpeg").scaledToHeight(150)
            wonder.setPixmap(pixmap)
            wonder.move(self.width() - pixmap.width(), self.height() - pixmap.height() - 30)
            wonder.resize(pixmap.width(), pixmap.height())
            wonder.show()
            self.wonder = wonder
        else:
            pixmap = QPixmap(f"wonders/{index}.jpeg").scaledToHeight(150)
            self.wonder.setPixmap(pixmap)

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
            card.show()
            off += 50
            self.cards.append(card)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.png'))
    game_data = GameData()
    gui = GameGUI(game_data=game_data)
    game_data.set_gui(gui)
    if len(gui.login) > 0:
        game_data.login = gui.login
    game_data.send_game_data_req()

    network_client = threading.Thread(target=client, args=(game_data,))
    network_client.start()

    gui.show()
    app.setQuitOnLastWindowClosed(True)
    app.exec_()
    queue.append(False)


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




