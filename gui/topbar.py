from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

WIDTH, HEIGHT = 1024, 768


class QTopBar(QLabel):
    def __init__(self, parent=None):
        super(QTopBar, self).__init__(parent)
        self.parent1 = parent
        self.move(0, 0)
        self.resize(WIDTH, 30)

        pixmap = QPixmap('topbar.jpg')
        self.setPixmap(pixmap)

        self.show()
        # self.lower()

        names = ['left', 'down', 'right']

        # self.left_indicator = QIcon(self.parent1, location=(30, 0), icon_name='left')
        # self.down_indicator = QIcon(self.parent1, location=(300, 0), icon_name='down')
        # self.right_indicator = QIcon(self.parent1, location=(500, 0), icon_name='right')

        self.indicators = []
        self.old_money, self.old_military, self.old_wins, self.old_loses = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
        self.new_money, self.new_military, self.new_wins, self.new_loses = [], [], [], []
        self.money = []
        self.military = []
        self.wins = []
        self.loses = []

        self.delta_test = None

        offset = 345
        for i in range(3):
            icon = QIcon(self.parent1, location=(30 + i*offset, 0), icon_name=names[i])
            self.indicators.append(icon)

            icon = QIcon(self.parent1, location=(30 + 30 + i*offset, 0), icon_name='money')
            icon = QIcon(self.parent1, location=(100 + 30 + i*offset, 0), icon_name='military')
            icon = QIcon(self.parent1, location=(170 + 30 + i*offset, 0), icon_name='wins')
            icon = QIcon(self.parent1, location=(240 + 30 + i*offset, 0), icon_name='loses')

            text = QText1(self.parent1, location=(30 + 30 + 30 + i*offset, 3), text='', color='yellow')
            self.money.append(text)

            text = QText1(self.parent1, location=(30 + 100 + 30 + i*offset, 3), text='', color='red')
            self.military.append(text)

            text = QText1(self.parent1, location=(30 + 170 + 30 + i*offset, 3), text='')
            self.wins.append(text)

            text = QText1(self.parent1, location=(30 + 240 + 30 + i*offset, 3), text='')
            self.loses.append(text)

        # self.update_data([3, 3, 3], [2, 1, 5], [1, 3, 3], [-2, -4, -2])

    def update_data(self, money=None, military=None, wins=None, loses=None, anim=True):
        self.update_money(money, anim)
        self.update_military(military, anim)
        self.update_wins(wins, anim)
        self.update_loses(loses, anim)

    def update_money(self, data, anim=False):
        if data is None:
            return
        for i in range(len(data)):
            delta = data[i] - self.old_money[i]
            if anim is True and delta != 0:
                print("Set money animation")
                self.money[i].set_animation(delta, data[i])
            else:
                print("Set money NO ANIM")
                self.money[i].setText(f'{data[i]}')
            self.old_money[i] = data[i]

    def update_military(self, data, anim=False):
        if data is None:
            return
        for i in range(len(data)):
            delta = data[i] - self.old_military[i]
            if anim is True and delta != 0:
                self.military[i].set_animation(delta, data[i])
            else:
                self.military[i].setText(f'{data[i]}')
            self.old_military[i] = data[i]

    def update_wins(self, data, anim=False):
        if data is None:
            return
        for i in range(len(data)):
            delta = data[i] - self.old_wins[i]
            if anim is True and delta != 0:
                self.wins[i].set_animation(delta, data[i])
            else:
                self.wins[i].setText(f'{data[i]}')
            self.old_wins[i] = data[i]

    def update_loses(self, data, anim=False):
        if data is None:
            return
        for i in range(len(data)):
            delta = data[i] - self.old_loses[i]
            if anim is True and delta != 0:
                self.loses[i].set_animation(delta, data[i])
            else:
                self.loses[i].setText(f'{data[i]}')
            self.old_loses[i] = data[i]


class QIcon(QLabel):
    def __init__(self, parent=None, location=(100, 100), icon_name='left'):
        super(QIcon, self).__init__(parent)
        self.parent1 = parent

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        pixmap = QPixmap(f'icons/{icon_name}.png').scaledToHeight(30)
        self.setPixmap(pixmap)

        self.move(location[0], location[1])
        self.show()


class QText1(QLabel):
    def __init__(self, parent=None, location=(100, 100), text='0', color='grey'):
        super(QText1, self).__init__(parent)

        self.parent1 = parent
        self.text = text

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        self.setFixedWidth(30)

        self.setText(text)
        self.setStyleSheet(f'color: {color}; font-size: 20px;')
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.setFont(my_font)

        self.anim = None
        self.animation = None

        self.move(location[0], location[1])
        self.show()

    def set_animation(self, delta, new_value):
        if delta > 0:
            color = 'green'
        else:
            color = 'red'
        self.anim = QText2(self.parent1, location=(self.x(), self.y()), text=f'{delta}', color=color)
        self.show()
        self.animation = QPropertyAnimation(self.anim, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(self.x(), self.y() + 40, 30, 30))
        self.animation.setEndValue(QRect(self.x(), self.y(), 30, 30))
        self.animation.finished.connect(lambda: self.anim.setParent(None))
        self.animation.finished.connect(lambda: self.setText(f'{new_value}'))
        self.animation.start()


class QText2(QLabel):
    def __init__(self, parent=None, location=(100, 100), text='0', color='grey'):
        super(QText2, self).__init__(parent)

        self.parent1 = parent
        self.text = text

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        self.setFixedWidth(30)

        self.setText(text)
        self.setStyleSheet(f'color: {color}; font-size: 25px;')
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.setFont(my_font)

        self.move(location[0], location[1])
        self.show()