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

    def update_data(self, money=None, military=None, wins=None, loses=None):
        self.update_money(money)
        self.update_military(military)
        self.update_wins(wins)
        self.update_loses(loses)

    def update_money(self, data):
        print("Money", data)
        if data is None:
            return
        for i in range(len(data)):
            print("money player", data[i])
            self.money[i].setText(f'{data[i]}')

    def update_military(self, data):
        if data is None:
            return
        for i in range(len(data)):
            self.military[i].setText(f'{data[i]}')

    def update_wins(self, data):
        if data is None:
            return
        for i in range(len(data)):
            self.wins[i].setText(f'{data[i]}')

    def update_loses(self, data):
        if data is None:
            return
        for i in range(len(data)):
            self.loses[i].setText(f'{data[i]}')

    def money_delta(self, delta):
        for d in delta:
            if d == 0:
                continue
            color = 'red' if d < 0 else 'green'
            self.delta_test = QText1(parent=self.parent1, location=(30 + 30 + 30 + 345, 50), text=str(d), color=color)
            self.delta_test.set_animation()
            self.delta_test.anim_start.start()

    def update_left_player(self, data):
        pass

    def update_down_player(self, data):
        pass

    def update_right_player(self, data):
        pass


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

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        self.setFixedWidth(30)

        self.setText(text)
        self.setStyleSheet(f'color: {color}; font-size: 20px;')
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.setFont(my_font)

        self.move(location[0], location[1])
        self.show()

    def set_animation(self):
        self.anim_start = QPropertyAnimation(self, b"geometry")
        self.anim_start.setDuration(2000)
        self.anim_start.setStartValue(QRect(30 + 30 + 30 + 345, 100, 30, 30))
        self.anim_start.setEndValue(QRect(30 + 30 + 30 + 345, 10, 30, 30))
        self.anim_start.finished.connect(lambda: self.setParent(None))
