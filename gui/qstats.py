from PyQt5.QtWidgets import QLabel


class QStats(QLabel):
    def __init__(self, parent=None):
        super(QStats, self).__init__(parent)
        self.vp = 0
        self.money = 0
        self.military = 0
        self.ready = 0
        self.setText(f'{self.vp} {self.money} {self.military}\n{self.ready}/3')

    def update_data(self, vp=None, money=None, military=None, ready=None):
        self.vp = vp if vp is not None else self.vp
        self.money = money if money is not None else self.money
        self.military = military if military is not None else self.military
        self.ready = ready if ready is not None else self.ready
        self.setText(f'{self.vp} {self.money} {self.military}\n{self.ready}/3')