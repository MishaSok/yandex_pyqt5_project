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
        self.teacher_class = TeacherForm()
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
                cursor.execute('SELECT password FROM users WHERE login=?', (login,))
                if cursor.fetchone() is None:
                    self.error_label.setText('Такого логина не существует')
                else:
                    for row in cursor.execute('SELECT password, role FROM users WHERE login=?', (login,)):
                        if row[0] == password:
                            if row[1] == 'Преподаватель':
                                self.teacher_class.add_login(login)
                                self.teacher_class.show()
                            else:
                                pass
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
            cursor.execute(f'SELECT login from users where login="{login}"')
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO users VALUES ('{name}', '{surname}', '{login}', '{password}', '{email}', '{role}', 0)")
                data_base.commit()
                if role == "Преподаватель":
                    cursor.execute(f"INSERT INTO teacher_stats VALUES ('{login}', 0, 0, 0)")
                    data_base.commit()
                self.close()
            else:
                print('Такой логин уже существует')
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


class TeacherForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_student_form = AddStudentForm()
        self.add_student_btn = QPushButton()
        self.login_label = QLabel()
        self.label_2 = QLabel()
        self.label_3 = QLabel()
        self.label_5 = QLabel()
        self.label_6 = QLabel()
        self.label_7 = QLabel()
        self.initUI()
        uic.loadUi('teacher_form.ui', self)
        self.label = QLabel()
        self.add_student_btn.clicked.connect(self.on_add_student_btn)

    def initUI(self):
        self.setGeometry(300, 400, 500, 500)
        self.setFixedSize(600, 500)

    def add_login(self, login):
        for row in cursor.execute('SELECT name, surname, password, email, role FROM users where login=?', (login,)):
            self.name, self.surname, self.login, self.password, \
            self.email, self.role = row[0], row[1], login, row[2], row[3], row[4]
        self.login_label.setText(self.login)
        self.label_2.setText(f'{self.name} {self.surname}')
        self.label_3.setText(f'{self.role}')
        self.update_teacher_stats()

    def update_teacher_stats(self):
        A = get_teacher_stats(cursor, self.login)
        self.label_5.setText(f'Учеников учится: {A[0]}')
        self.label_6.setText(f'Заданий выполнено: {A[1]}')
        self.label_7.setText(f'Заданий задано: {A[2]}')

    def on_add_student_btn(self):
        self.add_student_form.initialization(self.login)
        self.add_student_form.show()


class AddStudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.listWidget = QListWidget()
        self.add_btn = QPushButton()
        self.close_btn = QPushButton()
        uic.loadUi('add_student_form.ui', self)
        self.initUI()
        self.close_btn.clicked.connect(self.on_close_btn)
        self.add_btn.clicked.connect(self.on_add_btn)

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setFixedSize(340, 300)

    def initialization(self, login):
        print('test')
        self.login = login
        for row in cursor.execute("SELECT name, surname, login FROM users WHERE role='Ученик' AND have_teacher=0"):
            self.listWidget.addItem(f"{row[0]} {row[1]} ({row[2]})")
            print(row)

    def on_close_btn(self):
        self.listWidget.clear()
        self.close()

    def on_add_btn(self):
        try:
            self.student = self.listWidget.currentItem().text()
            res = str(self.student).split()[2].replace(')', '').replace('(', '')
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS teacher_{self.login}(
            student_login TEXT,
            student_name TEXT,
            student_surname TEXT);
            ''')
            data_base.commit()
            cursor.execute(f"INSERT INTO teacher_{self.login} VALUES ('{res}', '{str(self.student).split()[0]}', "
                           f"'{str(self.student).split()[1]}')")
            data_base.commit()
            cursor.execute(f"UPDATE users SET have_teacher=1 WHERE login='{res}'")
            data_base.commit()
            self.listWidget.clear()
            self.initialization(self.login)
        except Exception as Error:
            print(Error)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoginForm()
    ex.show()
    sys.exit(app.exec())
