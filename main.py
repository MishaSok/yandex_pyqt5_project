import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sqlite3
from reg_func import *

# Подключение к базе данных
data_base = sqlite3.connect('data_base.db', timeout=10)
cursor = data_base.cursor()


class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.register_form = RegisterForm()
        self.register_btn = QPushButton()
        self.join_btn = QPushButton()
        self.error_label = QLabel()
        self.login_line = QLineEdit()
        self.password_line = QLineEdit()
        self.initUI()
        self.setWindowTitle('test')
        uic.loadUi('login_form.ui', self)
        self.register_btn.clicked.connect(self.on_register_btn)
        self.join_btn.clicked.connect(self.on_join_btn)

    def initUI(self):
        self.setGeometry(300, 400, 300, 400)
        self.setFixedSize(300, 300)

    def on_register_btn(self):
        self.register_form.show()

    def on_join_btn(self):
        login = self.login_line.text()
        if login == '':
            self.error_label.setText('Введите логин')
        else:
            password = self.password_line.text()
            if password == '':
                self.error_label.setText('Введите пароль')
            else:
                cursor.execute('SELECT password FROM users WHERE login=?', (login, ))
                if cursor.fetchone() is None:
                    self.error_label.setText('Такого логина не существует')
                else:
                    for row in cursor.execute('SELECT password FROM users WHERE login=?', (login, )):
                        if row[0] == password:
                            self.error_label.setText('Успешная авторизация!')
                        else:
                            self.error_label.setText('Неверный пароль. Попробуйте снова')


class RegisterForm(QDialog):
    def __init__(self):
        super().__init__()
        self.register_button = QPushButton()
        self.cancel_button = QPushButton()
        self.req_btn = QPushButton()
        self.initUI()
        self.reqregform = ReqRegForm()
        uic.loadUi('register_form.ui', self)

        # Регистрация нажатий
        self.register_button.clicked.connect(self.on_reg_btn)
        self.cancel_button.clicked.connect(self.on_cancel_btn)
        self.req_btn.clicked.connect(self.on_req_btn)

    def initUI(self):
        self.setGeometry(800, 500, 300, 300)
        self.setFixedSize(300, 330)

    def on_reg_btn(self):
        name = self.lineEdit.text()
        surname = self.lineEdit_2.text()
        login = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        role = self.comboBox.currentText()
        errors = registration_rules(name, surname, login, password, email)
        if errors == '':
            cursor.execute(
                f"INSERT INTO users VALUES ('{name}', '{surname}', '{login}', '{password}', '{email}', '{role}')")
            data_base.commit()
            print('Успешная регистрация')
        else:
            self.reqregform.show()
            print('Ошибка регистрации:', errors)

    def on_cancel_btn(self):
        self.close()

    def on_req_btn(self):
        self.reqregform.show()


class ReqRegForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ok_btn = QPushButton()
        uic.loadUi('req_form.ui', self)
        self.ok_btn.clicked.connect(self.on_ok_btn)

    def initUI(self):
        self.setGeometry(800, 500, 300, 300)
        self.setFixedSize(300, 330)

    def on_ok_btn(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginForm()
    ex.show()
    sys.exit(app.exec())
