from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QDialogButtonBox


class QLoginDialog(QDialog):
    def __init__(self, parent=None):
        super(QLoginDialog, self).__init__(parent)
        layout = QVBoxLayout(self)

        self.setWindowTitle("Login")

        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)

        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def get_login_data(parent=None):
        dialog = QLoginDialog(parent)
        result = dialog.exec_()
        login = dialog.textName.text()
        password = dialog.textPass.text()
        return login, password, result == QDialog.Accepted
