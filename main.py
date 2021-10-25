import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle('test')
        uic.loadUi('login_form.ui', self)

    def initUI(self):
        self.setGeometry(300, 400, 300, 400)
        self.setFixedSize(300, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginForm()
    ex.show()
    sys.exit(app.exec())
