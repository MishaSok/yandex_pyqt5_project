import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.register_btn = QPushButton()
        self.initUI()
        self.setWindowTitle('test')
        uic.loadUi('login_form.ui', self)
        self.register_btn.clicked.connect(self.on_register_btn)

    def initUI(self):
        self.setGeometry(300, 400, 300, 400)
        self.setFixedSize(300, 300)

    def on_register_btn(self):
        print('test')
        self.register_form = RegisterForm()
        self.register_form.show()
        print('xui')


class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        uic.loadUi('register_form.ui', self)

    def initUI(self):
        self.setGeometry(800, 500, 300, 300)
        self.setFixedSize(300, 300)
        self.setWindowTitle('Регистрация')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginForm()
    ex.show()
    sys.exit(app.exec())
